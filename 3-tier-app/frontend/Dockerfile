FROM nginx:1.27-alpine
# The nginx image renders *.template files with env vars at container start
COPY default.conf.template /etc/nginx/templates/default.conf.template
COPY index.html app.js /usr/share/nginx/html/
ENV BACKEND_URL=http://backend:3000
EXPOSE 80
