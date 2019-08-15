default:
	make -i clean
	make build
	make run
	make logs

build:
	docker build -t bot-des-cons:0.1 .

run:
	docker run -d --name bot-des-cons --restart always bot-des-cons:0.1 $(DISCORD_TOKEN) $(LDP_TOKEN) $(MDP_TOKEN)

logs:
	docker logs -f bot-des-cons

clean:
	docker rm -f bot-des-cons
	docker rmi $(docker images --quiet --filter "dangling=true")
