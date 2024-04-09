#!/bin/bash

# 获取当前时间戳
CURRENT_TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# 设置要运行的 Docker 镜像名称
IMAGE_NAME="nezha123/titan-edge"

# 设置要启动的容器数量
NUM_CONTAINERS=5

# 设置 API 地址
API_URL="https://api-test1.container1.titannet.io/api/v2/device/binding"

# 从文件中读取提供的身份码
HASH_FILE="hashes.txt"

# 检查身份码文件是否存在
if [ ! -f "$HASH_FILE" ]; then
    echo "Error: Hash file $HASH_FILE not found."
    exit 1
fi

# 读取提供的身份码
HASHES=($(cat "$HASH_FILE"))

# 检查提供的身份码数量是否足够
NUM_HASHES=${#HASHES[@]}
if [ $NUM_HASHES -lt $NUM_CONTAINERS ]; then
    echo "Error: Not enough hashes provided. Expected $NUM_CONTAINERS, found $NUM_HASHES."
    exit 1
fi

# 循环启动多个容器
for ((i=0; i<$NUM_CONTAINERS; i++)); do
    # 从提供的身份码列表中获取身份码
    HASH=${HASHES[$i]}

    # 创建与容器对应的存储路径
    STORAGE_PATH="$HOME/.titanedge/container_$CURRENT_TIMESTAMP_$i"
    mkdir -p "$STORAGE_PATH"

    # 在后台运行容器，并将容器标识符保存到变量中
    CONTAINER_ID=$(docker run -d -v $STORAGE_PATH:/root/.titanedge --name "titan-edge-$CURRENT_TIMESTAMP-$i" $IMAGE_NAME)

    # 输出容器的标识符
    echo "Container $i started with ID: $CONTAINER_ID"

    # 绑定提供的身份码
    docker exec $CONTAINER_ID titan-edge bind --hash=$HASH $API_URL
done
