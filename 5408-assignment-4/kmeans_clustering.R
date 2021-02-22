library(ggplot2)
filedata <- (read.csv(file="E:/5408/python programs/timestamp.csv",header = FALSE))
timestamps <- filedata$V1
print(timestamps)
clusterdata <- kmeans(timestamps,8)
plotdata <- data.frame(v1=timestamps, cluster=factor(clusterdata$cluster))
print(clusterdata$centers)
ggplot(plotdata,aes(x=cluster, y=v1, color=cluster)) + geom_jitter()
