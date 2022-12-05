.PHONYS: deploy dev

PROJECT_ID = $(shell gcloud config get-value project)

install:
	@echo "Installing dependencies..."
	@npm install

dev: 
	@echo "Starting dev server"
	@LOCAL_DEV=true npm run dev

deploy:
	gcloud builds submit --tag gcr.io/$(PROJECT_ID)/listy-web --project $(PROJECT_ID)
