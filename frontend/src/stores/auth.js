import {defineStore} from 'pinia'
import {useApi} from '@/composables/useApi'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        token: localStorage.getItem('token'),
        isAuthenticated: false
    }),

    actions: {
        async login(credentials) {
            const {api} = useApi()

            try {
                const params = new URLSearchParams()
                params.append('username', credentials.email)
                params.append('password', credentials.password)

                const response = await api.post('/auth/login', params)

                const {access_token} = response.data

                this.token = access_token

                localStorage.setItem('token', access_token)

                try {
                    const userResponse = await api.get('/auth/users/me')
                    this.user = userResponse.data
                    this.isAuthenticated = true
                    return this.user
                } catch (fetchUserError) {
                    console.error("fetchUser failed immediately after login:", fetchUserError);
                    this.logout();
                    throw new Error("Login succeeded but failed to fetch user data.");
                }

            } catch (error) {
                this.logout()
                throw error
            }
        },

        async register(userData) {
            const {api} = useApi()

            const response = await api.post('/auth/register', userData)
            return response.data
        },

        async fetchUser() {
            const {api} = useApi()

            const response = await api.get('/auth/users/me')
            this.user = response.data
            this.isAuthenticated = true
            return response.data
        },

        async updateProfile(data) {
            const {api} = useApi()

            const response = await api.put('/auth/me', data)
            this.user = response.data
            return response.data
        },

        async updateProfilePicture(file) {
            const {api} = useApi()

            try {
                const presignedResponse = await api.post('/auth/me/image-upload-url', {
                    file_name: file.name,
                    content_type: file.type
                })

                const presignedUrlData = presignedResponse.data

                const formData = new FormData()
                Object.entries(presignedUrlData.fields).forEach(([key, value]) => {
                    formData.append(key, value)
                })
                formData.append('file', file)

                const uploadResponse = await fetch(presignedUrlData.url, {
                    method: 'POST',
                    body: formData
                })

                if (!uploadResponse.ok) {
                    throw new Error('Image upload failed')
                }

                await this.fetchUser()
                return this.user
            } catch (error) {
                console.error('Failed to upload profile image: ', error)
                throw error
            }

        },

        async forgotPassword(email) {
            const {api} = useApi()

            const response = await api.post('/auth/forgot-password', {email})
            return response.data
        },

        async resetPassword(token, newPassword) {
            const {api} = useApi()

            const response = await api.post('/auth/reset-password', {
                token,
                new_password: newPassword
            })
            return response.data
        },

        async logout() {
            const {api} = useApi()

            try {
                await api.post('/auth/logout')
            } catch (error) {
                console.error('Logout API call failed:', error)
            } finally {
                this.user = null
                this.token = null
                this.isAuthenticated = false
                localStorage.removeItem('token')
            }
        },

        async initializeAuth() {
            if (this.token) {
                await this.fetchUser()
            }
        }
    }
})