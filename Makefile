default:
	make -i clean
	make build
	make run
	make logs

build:
	docker build -t bot-des-cons:0.1 .

build-proxy:
	docker build --build-arg HTTP_PROXY="http://p-goodway:3128/" --build-arg HTTPS_PROXY="http://p-goodway:3128/" -t bot-des-cons:0.1 .

FILE=token.txt
TOKEN=`cat $(FILE)`

run:
	docker run -d --name bot-des-cons --restart always bot-des-cons:0.1 $(TOKEN)

logs:
	docker logs -f bot-des-cons

clean:
	docker rm -f bot-des-cons
	docker rmi $(docker images --quiet --filter "dangling=true")
