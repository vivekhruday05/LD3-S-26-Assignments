library(ggplot2)
library(dplyr)

data <- read.csv('/home/vivek/python/LD3/Assignments/3/71f9d8eeae726770d45e2a724fe3eb05_pset_1_data.csv')

sink('part2_output.txt')

cat("==== PART 2: R Data Analysis ====\n\n")

p1 <- ggplot(data, aes(x=RTlexdec)) + geom_histogram(bins=30, fill="blue", color="black", alpha=0.7) + theme_minimal() + labs(title="Histogram of RTs", x="Lexical Decision RT", y="Count")
ggsave('hist_rts.png', plot=p1, width=6, height=4)

p2 <- ggplot(data, aes(x=RTlexdec, fill=AgeSubject)) + geom_histogram(bins=30, color="black", alpha=0.7, position="identity") + facet_wrap(~AgeSubject) + theme_minimal() + labs(title="Histograms for Young and Old Subjects", x="Lexical Decision RT", y="Count")
ggsave('hist_age.png', plot=p2, width=8, height=4)

young_data <- data %>% filter(AgeSubject == "young")

young_rts <- young_data$RTlexdec[!is.na(young_data$RTlexdec)]
z_scores <- (young_rts - mean(young_rts)) / sd(young_rts)

obs_1_sd <- sum(abs(z_scores) < 1) / length(z_scores)
obs_2_sd <- sum(abs(z_scores) < 2) / length(z_scores)
obs_3_sd <- sum(abs(z_scores) < 3) / length(z_scores)

exp_1_sd <- 0.6827
exp_2_sd <- 0.9545
exp_3_sd <- 0.9973

cat("Z-Score Analysis for Young Subjects:\n")
cat(sprintf("Observed within 1 SD: %.4f (Expected: %.4f)\n", obs_1_sd, exp_1_sd))
cat(sprintf("Observed within 2 SD: %.4f (Expected: %.4f)\n", obs_2_sd, exp_2_sd))
cat(sprintf("Observed within 3 SD: %.4f (Expected: %.4f)\n\n", obs_3_sd, exp_3_sd))

cat("Mean vs Median Comparison for Young Subjects:\n")
cat(sprintf("RTlexdec - Mean: %.4f, Median: %.4f\n", mean(young_data$RTlexdec, na.rm=T), median(young_data$RTlexdec, na.rm=T)))
cat(sprintf("NounFrequency - Mean: %.4f, Median: %.4f\n\n", mean(young_data$NounFrequency, na.rm=T), median(young_data$NounFrequency, na.rm=T)))

young_data$Starts_P <- grepl("^p", young_data$Word, ignore.case=TRUE)
p_words <- young_data %>% filter(Starts_P == TRUE) %>% pull(RTlexdec)
other_words <- young_data %>% filter(Starts_P == FALSE) %>% pull(RTlexdec)

t_test_p <- t.test(p_words, other_words)
cat("T-test comparing 'p' words vs others:\n")
print(t_test_p)
cat("\n")

nv_data <- data %>% filter(WordCategory %in% c("N", "V"))

p3 <- ggplot(nv_data, aes(x=WordCategory, y=RTlexdec, fill=WordCategory)) + geom_boxplot() + theme_minimal() + labs(title="Boxplot of RTs by Noun/Verb", x="Word Category", y="Lexical Decision RT")
ggsave('boxplot_nv.png', plot=p3, width=6, height=4)

nv_summary <- nv_data %>% group_by(WordCategory) %>% summarize(MeanRT = mean(RTlexdec, na.rm=TRUE))
p4 <- ggplot(nv_summary, aes(x=WordCategory, y=MeanRT, fill=WordCategory)) + geom_bar(stat="identity") + theme_minimal() + labs(title="Bar Plot of Mean RTs by Noun/Verb", x="Word Category", y="Mean Lexical Decision RT")
ggsave('barplot_nv.png', plot=p4, width=6, height=4)

data$InitialLetter <- toupper(substr(data$Word, 1, 1))
p5 <- ggplot(data, aes(x=InitialLetter, y=RTlexdec, fill=InitialLetter)) + geom_boxplot() + theme_minimal() + labs(title="Boxplot of RTs by Initial Letter", x="Initial Letter", y="Lexical Decision RT") + theme(legend.position="none")
ggsave('boxplot_initial.png', plot=p5, width=10, height=4)

vowels <- c('a', 'e', 'i', 'o', 'u')
has_two_cons <- sapply(data$Word, function(w) {
  if(nchar(as.character(w)) < 2) return(FALSE)
  c1 <- substr(tolower(w), 1, 1)
  c2 <- substr(tolower(w), 2, 2)
  return((!c1 %in% vowels) & (!c2 %in% vowels) & c1 %in% letters & c2 %in% letters)
})

data$TwoConsonants <- has_two_cons
two_cons_rts <- data$RTlexdec[data$TwoConsonants]
other_rts <- data$RTlexdec[!data$TwoConsonants]

t_test_cons <- t.test(two_cons_rts, other_rts)
cat("T-test comparing words starting with 2 consonants vs others:\n")
print(t_test_cons)

p6 <- ggplot(data, aes(x=TwoConsonants, y=RTlexdec, fill=TwoConsonants)) + geom_boxplot() + theme_minimal() + labs(title="Boxplot of RTs by Initial Consonants", x="Starts with Two Consonants", y="Lexical Decision RT")
ggsave('boxplot_cons.png', plot=p6, width=6, height=4)

sink()
