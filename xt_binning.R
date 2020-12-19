library("rjson")
library("dplyr")
library(ggplot)
library(ggsoccer)

data <- fromJSON(file = "expected_threat.json")
data <- t(array(unlist(data), dim = c(12, 8))) ###this is where the error was, the xt data was being read in the wrong dimensions

df <- data.frame(matrix(runif(400), ncol=4))*100
colnames(df) <- c("x1", "y1", "x2", "y2")

df <- df %>% mutate(x1_bin = ntile(x1, 12)) %>% 
             mutate(x2_bin = ntile(x2, 12)) %>%
             mutate(y1_bin = ntile(y1, 8)) %>% 
             mutate(y2_bin = ntile(y2, 8))
df <- cbind(df, start_val = mapply(function(x,y) data[y,x], df$x1_bin, df$y1_bin))
df <- cbind(df, end_val = mapply(function(x,y) data[y,x], df$x2_bin, df$y2_bin))

df$xt_value <- (df$end_val - df$start_val)

###plot all passes to check
ggplot(df) + 
annotate_pitch() +
geom_segment(aes(x=x1, y=y1, xend=x2, yend=y2, colour=xt_value),arrow= arrow(length=unit(0.08, 'inches')))
