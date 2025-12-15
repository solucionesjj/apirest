docker run -d \
		--name mysql-container \
		-e MYSQL_ROOT_PASSWORD=Root12345 \
		-e MYSQL_DATABASE=Sistema \
		-v mysql_data:/var/lib/mysql \
		-p 3306:3306 \
		mysql:8.0