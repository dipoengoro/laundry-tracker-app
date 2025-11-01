import { defineStore } from 'pinia'
import { useApi } from '@/composables/useApi'

export const useClothingStore = defineStore('clothing', {
  state: () => ({
    clothes: [],
    loading: false,
    presignedUrlCache: {},
    presignedUrlExpiry: {},
  }),

  actions: {
  
    async fetchClothes() {
      const { api } = useApi()
      this.loading = true
      
      try {
        const response = await api.get('/pakaian/')
        this.clothes = response.data;
        console.log(this.clothes);
      } catch (error) {
        console.error('Failed to fetch clothes:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async getClothingById(id) {
      const { api } = useApi()
      const now = Date.now()

      try {
        const response = await api.get(`/pakaian/${id}`)
        const clothing = response.data

        if (this.presignedUrlCache[id] && this.presignedUrlExpiry[id] > now) {
          clothing.foto_url = this.presignedUrlCache[id]
        } else if (clothing.foto_url) {
          const presignedResponse = await api.get(`/pakaian/${id}`)
          clothing.foto_url = presignedResponse.data.foto_url
          this.presignedUrlCache[id] = clothing.foto_url
          this.presignedUrlExpiry[id] = now + 14 * 60 * 1000
        }

        return clothing;
      } catch (error) {
        console.error('Failed to fetch clothing:', error)
        throw error
      }
    },

    async createClothing(clothingData) {
      const { api } = useApi()
      
      try {
        const response = await api.post('/pakaian/', clothingData)
        const newClothing = response.data
        this.clothes.push(newClothing)
        return newClothing
      } catch (error) {
        console.error('Failed to create clothing:', error)
        throw error
      }
    },

    async updateClothing(id, clothingData) {
      const { api } = useApi()
      
      try {
        const response = await api.put(`/pakaian/${id}`, clothingData)
        const index = this.clothes.findIndex(c => c.id === id)
        if (index !== -1) {
          this.clothes[index] = response.data
        }
        return response.data
      } catch (error) {
        console.error('Failed to update clothing:', error)
        throw error
      }
    },

    async deleteClothing(id) {
      const { api } = useApi()
      
      try {
        await api.delete(`/pakaian/${id}`)
        this.clothes = this.clothes.filter(c => c.id !== id)
      } catch (error) {
        console.error('Failed to delete clothing:', error)
        throw error
      }
    },
  }
})