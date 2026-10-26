FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY public /usr/share/nginx/html/public
COPY admin /usr/share/nginx/html/admin
COPY dosen /usr/share/nginx/html/dosen
COPY mahasiswa /usr/share/nginx/html/mahasiswa
COPY static /usr/share/nginx/html/static
EXPOSE 80
