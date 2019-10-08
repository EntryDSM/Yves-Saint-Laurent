#!/usr/bin/env bash

version=`python -c "import ysl; print(ysl.__version__)"`

echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin registry.entrydsm.hs.kr

if [[ "$1" == "develop" ]];then
    echo "Docker build on develop started"

    docker build -t registry.entrydsm.hs.kr/ysl:develop .

    docker push registry.entrydsm.hs.kr/ysl:develop

    echo "Docker image pushed"

elif [[ "$1" == "master" ]];then
    echo "Docker build on master started"

    docker build -t registry.entrydsm.hs.kr/ysl:${version} .

    docker tag registry.entrydsm.hs.kr/ysl:${version} registry.entrydsm.hs.kr/ysl:latest

    docker push registry.entrydsm.hs.kr/ysl:${version}
    docker push registry.entrydsm.hs.kr/ysl:latest

    echo "Docker image pushed"

fi

exit 0