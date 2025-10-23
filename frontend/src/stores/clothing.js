import { defineStore } from 'pinia'
import { useApi } from '@/composables/useApi'
import { normalizedDataClothing } from '../utils/helpers'


export const useClothingStore = defineStore('clothing', {
  state: () => ({
    clothes: [],
    loading: false
  }),

  actions: {
  
    async fetchClothes() {
      const { api } = useApi()
      this.loading = true
      
      try {
        const response = await api.get('/pakaian/')
        this.clothes = response.data.map(normalizedDataClothing);
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
      
      try {
        const response = await api.get(`/pakaian/${id}`)
        console.log(response.data);
        return normalizedDataClothing(response.data);
      } catch (error) {
        console.error('Failed to fetch clothing:', error)
        throw error
      }
    },

    async createClothing(clothingData) {
      const { api } = useApi()
      
      try {
        const response = await api.post('/pakaian/', clothingData)
        const newClothing = normalizedDataClothing(response.data)
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

    async uploadClothingImage(clothingId, file) {
      const { api } = useApi()
      
      try {
        const formData = new FormData()
        formData.append('file', file)
        
        const response = await api.post(`/pakaian/${clothingId}/image`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        // Update local state
        const index = this.clothes.findIndex(c => c.id === clothingId)
        if (index !== -1) {
          this.clothes[index] = response.data
        }
        
        return response.data
      } catch (error) {
        console.error('Failed to upload clothing image:', error)
        throw error
      }
    }
  }
})