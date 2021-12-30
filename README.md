![Image](https://github.com/odrusso/eduace/blob/master/docs/resources/logo_small.png)

![Build](https://github.com/odrusso/eduace/actions/workflows/backend.yaml/badge.svg)
![Build](https://github.com/odrusso/eduace/actions/workflows/frontend.yaml/badge.svg)
![Build](https://github.com/odrusso/eduace/actions/workflows/infra.yaml/badge.svg)


## Getting started
### Frontend
`cd web && npm i` - setup the prereqs    
`cd web && npm run mock` - to start the React app with a MSW mock API  
`cd web && npm run start` - to start the React app pointing at a real API  

### Backend
#### Using Flask dev-server
`cd ..` - get back to root directory  
`export FLASK_ENV='development'` - set up required environment variables. You may wish to set these in your `.(zsh|bash)rc` file.  
`export FLASK_APP='api'`  
`export FLASK_DEBUG='True'`  
`pip install -r requirements.txt` - install Python reqs, you may like to contain the dependencies in a virtualenv  
`flask run` - start the backend development server  

#### Using Docker
`docker build -t eduace-api:latest .` - build the image
`docker container run -p [port-you-want-in-localhost]:80 eduace-api` - run the image
