# frontend/Dockerfile
FROM node:20
WORKDIR /app

# copy package files untuk cache layer
COPY package*.json ./

# install dependencies (tidak butuh package-lock.json)
RUN npm install --legacy-peer-deps

# optional: enable corepack
RUN corepack enable

# copy source app
COPY . .

# start dev server (vite) dan expose host agar dapat diakses dari host machine
CMD ["npm", "run", "dev", "--", "--host"]
