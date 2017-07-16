# Kolmogorov-Smirnov test
filename = paste("/Users/phayate/src/metrics-data/Derby/mergedMetrics10.9.csv")
df1 <- read.table( filename, header = T, sep=",")
filename = paste("/Users/phayate/src/metrics-data/Derby/mergedMetrics10.10.csv")
df2 <- read.table( filename, header = T, sep=",")
kstest <- function(df1,df2) {
  ks.test(df1$pc1, df2$pc1)
  ks.test(df1$pc2, df2$pc2)
  ks.test(df1$pc3, df2$pc3)
  ks.test(df1$pc4, df2$pc4)
  ks.test(df1$pd1, df2$pd1)
  ks.test(df1$pd2, df2$pd2)
  ks.test(df1$pd3, df2$pd3)
  ks.test(df1$pd4, df2$pd4)
  ks.test(df1$pd5, df2$pd5)
  ks.test(df1$pd6, df2$pd6)
  ks.test(df1$fault, df2$fault)
}
