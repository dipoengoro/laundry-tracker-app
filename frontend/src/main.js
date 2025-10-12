import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './index.css'

const app = createApp(App)

// Cukup pasang Pinia dan Router, lalu mount.
// Tidak ada logika store atau guard di sini.
app.use(createPinia())
app.use(router)

app.mount('#app')