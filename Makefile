default: build

build:
	docker build -t techiaith/festival-tts-cy-api .

run:
	rm -rf log
	mkdir -p log
	docker run -d --name festival-tts-cy-api \
	-p 4321:8008 \
	-v ${PWD}/log:/var/log/festival \
	techiaith/festival-tts-cy-api

stop:
	-docker stop festival-tts-cy-api 
	-docker rm festival-tts-cy-api 

clean:
	-docker rmi techiaith/festival-tts-cy-api

