#!/usr/bin/env bash

version = `"python -c import ysl; print(ysl.__version__)"`

echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin registry.entrydsm.hs.kr

if [[ "$1" == "api" ]];then
    echo "Docker build on dev startred"

    docker build -t registry.entrydsm.hs.kr/ysl:dev.

    docker push registry.entrydsm.hs.kr/ysl:dev

elif [["$1" == "master"]];then
    echo "Docker build on master started"

    docker build -t registry.entrydsm.hs.kr/ysl:${version} .

    docker tag registry.entrydsm.hs.kr/ysl:${version} registry.entrydsm.hs.kr/ysl:latest

    docker push registry.entrydsm.hs.kr/ysl:${version}
    docker push registry.entrydsm.hs.kr/ysl:latest

fi

exit 0
