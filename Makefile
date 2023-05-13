default: build

build:
	docker build -t techiaith/festival-tts-api .

run:
	rm -rf log
	mkdir -p log
	docker run -d --name festival-tts-api \
	-p 4321:8008 \
	-v ${PWD}/log:/var/log/festival \
	techiaith/festival-tts-api

stop:
	-docker stop festival-tts-api 
	-docker rm festival-tts-api 

clean:
	-docker rmi techiaith/festival-tts-api

