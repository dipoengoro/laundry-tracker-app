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
        path: '/laundry-sessions',
        icon: '🧺'
    },
    {
        name: 'Profile',
        path: '/profile',
        icon: '👤'
    }
]

export const CLOTHING_CATEGORIES = [
    'Top',
    'Bottom',
    'Underwear',
    'Outwear',
    'Accessory'
]

export const CLOTHING_TYPES = [
    'Shirt',
    'T-Shirt',
    'Pants',
    'Shorts',
    'Skirt',
    'Dress',
    'Jacket',
    'Sweater',
    'Jeans',
    'Socks'
]

export const CLOTHING_COLORS = [
    'White',
    'Black',
    'Red',
    'Blue',
    'Green',
    'Yellow',
    'Purple',
    'Pink',
    'Gray',
    'Brown',
    'Beige'
]

export const CLOTHING_MATERIALS = [
    'Cotton',
    'Polyester',
    'Denim',
    'Silk',
    'Wool',
    'Linen',
    'Rayon',
    'Spandex',
    'Blend'
]

export const LAUNDRY_STATUSES = [
    {
        value: 'Received',
        label: 'Received',
        color: 'blue',
        description: 'Clothing has been received'
    },
    {
        value: 'Washing',
        label: 'Washing',
        color: 'indigo',
        description: 'Currently in the washing process'
    },
    {
        value: 'Drying',
        label: 'Drying',
        color: 'purple',
        description: 'Currently in the drying process'
    },
    {
        value: 'Ironing',
        label: 'Ironing',
        color: 'pink',
        description: 'Currently in the ironing process'
    },
    {
        value: 'Completed',
        label: 'Completed',
        color: 'green',
        description: 'Processing is complete'
    },
    {
        value: 'Taken',
        label: 'Taken',
        color: 'gray',
        description: 'Taken by owner'
    }
]