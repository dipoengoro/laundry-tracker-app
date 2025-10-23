export const API_BASE_URL = 'http://localhost:8000'

export const NAVIGATION_ITEMS = [
  {
    name: 'Dashboard',
    path: '/dashboard',
    icon: '🏠'
  },
  {
    name: 'My Clothes',
    path: '/clothing',
    icon: '👕'
  },
  {
    name: 'Laundry Sessions',
    path: '/laundry',
    icon: '🧺'
  },
  {
    name: 'Profile',
    path: '/profile',
    icon: '👤'
  }
]

export const CLOTHING_CATEGORIES = [
  'Atasan',
  'Bawahan',
  'Dalam',
  'Luar',
  'Aksesoris'
]

export const CLOTHING_TYPES = [
  'Kemeja',
  'T-Shirt',
  'Kaos',
  'Celana Panjang',
  'Celana Pendek',
  'Rok',
  'Dress',
  'Jaket',
  'Sweater',
  'Jeans'
]

export const CLOTHING_COLORS = [
  'Putih',
  'Hitam',
  'Merah',
  'Biru',
  'Hijau',
  'Kuning',
  'Ungu',
  'Pink',
  'Abu-abu',
  'Coklat'
]

export const CLOTHING_MATERIALS = [
  'Katun',
  'Polyester',
  'Denim',
  'Sutra',
  'Wol',
  'Linen',
  'Rayon',
  'Spandex',
  'Campuran'
]

export const LAUNDRY_STATUSES = [
  {
    value: 'Diterima',
    label: 'Diterima',
    color: 'blue',
    description: 'Pakaian telah diterima'
  },
  {
    value: 'Dicuci',
    label: 'Dicuci',
    color: 'indigo',
    description: 'Sedang dalam proses pencucian'
  },
  {
    value: 'Dikeringkan',
    label: 'Dikeringkan',
    color: 'purple',
    description: 'Sedang dalam proses pengeringan'
  },
  {
    value: 'Disetrika',
    label: 'Disetrika',
    color: 'pink',
    description: 'Sedang dalam proses penyetrikaan'
  },
  {
    value: 'Selesai',
    label: 'Selesai',
    color: 'green',
    description: 'Sudah selesai diproses'
  },
  {
    value: 'Diambil',
    label: 'Diambil',
    color: 'gray',
    description: 'Sudah diambil pemilik'
  }
]