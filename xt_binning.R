library("rjson")
library("dplyr")

result <- fromJSON(file = "C:\\code_repository\\python_files\\ExpectedPossessionValue\\expected_threat.json")
result <- array(unlist(L), dim = c(8, 12))

df <- data.frame(matrix(runif(400), ncol=4))*100
colnames(df) <- c("x1", "y1", "x2", "y2")

df <- df %>% mutate(x1_bin = ntile(x1, 12)) %>% 
             mutate(x2_bin = ntile(x2, 12)) %>%
             mutate(y1_bin = ntile(y1, 8)) %>% 
             mutate(y2_bin = ntile(y2, 8))
df <- cbind(df, start_val = mapply(function(x,y) result[y,x], df$x1_bin, df$y1_bin))
df <- cbind(df, end_val = mapply(function(x,y) result[y,x], df$x2_bin, df$y2_bin))

df$xt_value <- (df$end_val - df$start_val)

