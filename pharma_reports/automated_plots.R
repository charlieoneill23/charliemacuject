library(googledrive)
library(ggplot2)
library(forestmangr)
library(plotrix)
drive_find(n=5)
drive_path = "pharma_reports/EricMayer/"

# INITIAL METRICS
drive_download("pharma_reports/EricMayer/initialmetrics.csv",
               path = "/Users/charlesoneill/Documents/Macuject/Drive_API/initialmetrics.csv",
               overwrite = TRUE)
met <- read.csv("/Users/charlesoneill/Documents/Macuject/Drive_API/initialmetrics.csv")
met$LucentisInit.

## INITIATION_DRUG
pdf(file = "/Users/charlesoneill/Documents/Macuject/Drive_API/initiation_drug.pdf")
# create dummy data
pieval<-c(met$LucentisInit., met$EyleaInit., met$AvastinInit.)
pielabels<-paste0(round(pieval/sum(pieval) * 100, 2), "%")
labels = c("Lucentis", "Eylea", "Avastin")
pie3D(pieval,radius=1,labels=pielabels,explode=0.05,
      col = c("skyblue", "#E69F00", "#1589FF", "#999999"))
legend("bottomleft", 
       legend = c("Lucentis", "Eylea", "Avastin"), 
       col = c("skyblue", "#E69F00", "#1589FF", "#999999"), 
       pch = c(19,19,19,19), 
       bty = "n", 
       pt.cex = 2, 
       cex = 1.2, 
       text.col = "black", 
       horiz = F , 
       inset = c(0.05, 0.06))
dev.off()
drive_upload("/Users/charlesoneill/Documents/Macuject/Drive_API/initiation_drug.pdf",
             path = paste(drive_path, "initiation_drug.csv"))


# VISUAL METRICS
drive_download("pharma_reports/EricMayer/visual_metrics.csv",
               path = "/Users/charlesoneill/Documents/Macuject/Drive_API/visual_metrics.csv",
               overwrite = TRUE)
initmet <- read.csv("/Users/charlesoneill/Documents/Macuject/Drive_API/visual_metrics.csv")

## PVI_BYDRUG
pdf(file = "/Users/charlesoneill/Documents/Macuject/Drive_API/PVI_bydrug.pdf")
# create dummy data
sub_df = initmet[c(0, 1, 2, 3),] 
sub_df = round_df(sub_df, digits=2, rf = "round")
data <- data.frame(
  Drug=c('Lucentis', 'Eylea', 'Multiple'),
  value=sub_df$PVI,
  sd=sub_df$PVI_sd
)
# Most basic error bar
cbPalette <- c("#56B4E9", "#E69F00", "#FFFFFF", "#999999")
ggplot(data, aes(x=Drug, y=value, fill=Drug)) +
  geom_bar( aes(x=Drug, y=value), stat="identity",
            alpha=0.8, width = 0.5) +
  geom_errorbar( aes(x=Drug, ymin=value-sd, ymax=value+sd), 
                 width=0.2, colour="black", alpha=0.9, size=0.7) +
  scale_fill_manual(values=c("skyblue", "#E69F00", "#1589FF", "#999999")) + 
  geom_text(aes(label=value), position=position_dodge(width=0.9), 
            vjust=12) +
  labs(title="Peak visual improvement by drug",x="Drug", 
       y = "LogMAR letters") +
  theme_classic()
dev.off()
drive_upload("/Users/charlesoneill/Documents/Macuject/Drive_API/PVI_bydrug.pdf",
             path = paste(drive_path, "PVI_bydrug.csv"))




## PVI_BYIMPROVEMENT
pdf(file = "/Users/charlesoneill/Documents/Macuject/Drive_API/PVI_byimprovement.pdf")
# create data
sub_df = initmet[c(0, 4, 6),] 
sub_df = round_df(sub_df, digits=2, rf = "round")
data <- data.frame(
  Drug=c('Patients who improved', 'Overall'),
  value=sub_df$PVI,
  sd=sub_df$PVI_sd
)
# Most basic error bar
cbPalette <- c("#56B4E9", "#E69F00", "#FFFFFF", "#999999")
ggplot(data, aes(x=Drug, y=value, fill=Drug)) +
  geom_bar( aes(x=Drug, y=value), stat="identity",
            alpha=0.8, width = 0.5) +
  geom_errorbar( aes(x=Drug, ymin=value-sd, ymax=value+sd), 
                 width=0.2, colour="black", alpha=0.9, size=0.7) +
  scale_fill_manual(values=c("skyblue", "#E69F00", "#1589FF", "#999999")) + 
  geom_text(aes(label=value), position=position_dodge(width=0.9), 
            vjust=11) +
  labs(title="Comparing PVI of those who improved vs overall",x="Improvement", 
       y = "PVI (LogMAR letters)") +
  theme_classic()
dev.off()
drive_upload("/Users/charlesoneill/Documents/Macuject/Drive_API/PVI_byimprovement.pdf",
             path = paste(drive_path, "PVI_byimprovement.csv"))



# TPVI_BYDRUG
pdf(file = "/Users/charlesoneill/Documents/Macuject/Drive_API/TPVI_bydrug.pdf")
# create data
sub_df = initmet[c(0, 1, 2, 3),] 
sub_df = round_df(sub_df, digits=0, rf = "round")
data <- data.frame(
  Drug=c('Lucentis', 'Eylea', 'Multiple'),
  value=sub_df$TPVI,
  sd=sub_df$TPVI_sd
)
# Most basic error bar
cbPalette <- c("#56B4E9", "#E69F00", "#FFFFFF", "#999999")
ggplot(data, aes(x=Drug, y=value, fill=Drug)) +
  geom_bar( aes(x=Drug, y=value), stat="identity",
            alpha=0.8, width = 0.5) +
  scale_fill_manual(values=c("skyblue", "#E69F00", "#1589FF", "#999999")) + 
  geom_text(aes(label=value), position=position_dodge(width=0.9), 
            vjust=11) +
  labs(title="Time to best vision by single or multiple drugs",x="Drug", 
       y = "Days since starting treatment") +
  theme_classic()
dev.off()
drive_upload("/Users/charlesoneill/Documents/Macuject/Drive_API/TPVI_bydrug.pdf",
             path = paste(drive_path, "TPVI_bydrug.csv"))


## VLP_BYDRUG
pdf(file = "/Users/charlesoneill/Documents/Macuject/Drive_API/VLP_bydrug.pdf")
# create data
sub_df = initmet[c(0, 1, 2, 3),] 
sub_df = round_df(sub_df, digits=2, rf = "round")
data <- data.frame(
  Drug=c('Lucentis', 'Eylea', 'Multiple'),
  value=sub_df$VLP,
  sd=sub_df$VLP_sd
)
# Most basic error bar
cbPalette <- c("#56B4E9", "#E69F00", "#FFFFFF", "#999999")
ggplot(data, aes(x=Drug, y=value, fill=Drug)) +
  geom_bar( aes(x=Drug, y=value), stat="identity",
            alpha=0.8, width = 0.5) +
  geom_errorbar( aes(x=Drug, ymin=value-sd, ymax=value+sd), 
                 width=0.2, colour="black", alpha=0.9, size=0.7) +
  scale_fill_manual(values=c("skyblue", "#E69F00", "#1589FF", "#999999")) + 
  geom_text(aes(label=value), position=position_dodge(width=0.9), 
            vjust=16) +
  labs(title="Vision loss from peak, by drug",x="Drug", 
       y = "LogMAR letters") +
  theme_classic()
dev.off()
drive_upload("/Users/charlesoneill/Documents/Macuject/Drive_API/VLP_bydrug.pdf",
             path = paste(drive_path, "VLP_bydrug.csv"))



## VLP_BYIMPROVEMENT
pdf(file = "/Users/charlesoneill/Documents/Macuject/Drive_API/VLP_byimprovement.pdf")
# create data
sub_df = initmet[c(0, 4, 5, 6),] 
sub_df = round_df(sub_df, digits=2, rf = "round")
data <- data.frame(
  Drug=c('Improved', 'Didn\'t improve', 'Overall'),
  value=sub_df$VLP,
  sd=sub_df$VLP_sd
)
# Most basic error bar
cbPalette <- c("#56B4E9", "#E69F00", "#FFFFFF", "#999999")
ggplot(data, aes(x=Drug, y=value, fill=Drug)) +
  geom_bar( aes(x=Drug, y=value), stat="identity",
            alpha=0.8, width = 0.5) +
  geom_errorbar( aes(x=Drug, ymin=value-sd, ymax=value+sd), 
                 width=0.2, colour="black", alpha=0.9, size=0.7) +
  scale_fill_manual(values=c("skyblue", "#E69F00", "#1589FF", "#999999")) + 
  geom_text(aes(label=value), position=position_dodge(width=0.9), 
            vjust=11) +
  labs(title="Comparing VLP of those who improved vs overall",x="Improvement", 
       y = "LogMAR letters") +
  theme_classic()
dev.off()
drive_upload("/Users/charlesoneill/Documents/Macuject/Drive_API/VLP_byimprovement.pdf",
             path = paste(drive_path, "VLP_byimprovement.csv"))




## OVC_BYDRUG
pdf(file = "/Users/charlesoneill/Documents/Macuject/Drive_API/OVC_bydrug.pdf")
# create data
sub_df = initmet[c(0, 1, 2, 3),] 
sub_df = round_df(sub_df, digits=2, rf = "round")
data <- data.frame(
  Drug=c('Lucentis', 'Eylea', 'Multiple'),
  value=sub_df$OVC,
  sd=sub_df$OVC_sd
)
# Most basic error bar
cbPalette <- c("#56B4E9", "#E69F00", "#FFFFFF", "#999999")
ggplot(data, aes(x=Drug, y=value, fill=Drug)) +
  geom_bar( aes(x=Drug, y=value), stat="identity",
            alpha=0.8, width = 0.5) +
  scale_fill_manual(values=c("skyblue", "#E69F00", "#1589FF", "#999999")) + 
  geom_text(aes(label=value), position=position_dodge(width=0.9), 
            vjust=11) +
  labs(title="Overall visual change (OVC) by drug",x="Drug", 
       y = "LogMAR letters") +
  theme_classic()
dev.off()
drive_upload("/Users/charlesoneill/Documents/Macuject/Drive_API/OVC_bydrug.pdf",
             path = paste(drive_path, "OVC_bydrug.csv"))



## OVC_BYIMPROVEMENT
pdf(file = "/Users/charlesoneill/Documents/Macuject/Drive_API/OVC_byimprovement.pdf")
# create data
sub_df = initmet[c(0, 4, 5, 6),] 
sub_df = round_df(sub_df, digits=2, rf = "round")
data <- data.frame(
  Drug=c('Improved', 'Didn\'t improve', 'Overall'),
  value=sub_df$OVC,
  sd=sub_df$OVC_sd
)
# Most basic error bar
cbPalette <- c("#56B4E9", "#E69F00", "#FFFFFF", "#999999")
ggplot(data, aes(x=Drug, y=value, fill=Drug)) +
  geom_bar( aes(x=Drug, y=value), stat="identity",
            alpha=0.8, width = 0.5) +
  geom_errorbar( aes(x=Drug, ymin=value-sd, ymax=value+sd), 
                 width=0.2, colour="black", alpha=0.9, size=0.7) +
  scale_fill_manual(values=c("skyblue", "#E69F00", "#1589FF", "#999999")) + 
  geom_text(aes(label=value), position=position_dodge(width=0.9), 
            vjust=11) +
  labs(title="Comparing OVC of those who improved vs overall",
       x="Improvement", 
       y = "LogMAR letters") +
  theme_classic()
dev.off()
drive_upload("/Users/charlesoneill/Documents/Macuject/Drive_API/OVC_byimprovement.pdf",
             path = paste(drive_path, "OVC_byimprovement.csv"))



# ANCHOR PLOT
drive_download("pharma_reports/EricMayer/anchor.csv",
               path = "/Users/charlesoneill/Documents/Macuject/Drive_API/anchor.csv",
               overwrite = TRUE)
anchor <- read.csv("/Users/charlesoneill/Documents/Macuject/Drive_API/anchor.csv")
pdf(file = "/Users/charlesoneill/Documents/Macuject/Drive_API/anchor_plot.pdf")
x <- anchor$Month
rani5 <- anchor$Ranibizumab_0.5mg
rani3 <- anchor$Ranibizumab_0.3mg
doctor  <- anchor$Doctor_Mean
# add initial plot
plot(x, doctor, type = "b", frame = TRUE, pch = 19, 
     col = "orange", xlab = "Months since initiation", 
     ylab = "Visual improvement (LogMAR letters)", xaxt="n",
     ylim=c(-1.5, 12))
axis(side = 1, at = x,labels = T)
# Add a second line
lines(x, rani5, pch = 18, col = "skyblue", type = "b", lty = 2)
# Add a third line
lines(x, rani3, pch = 18, col = "gray", type = "b", lty = 2)
# Add a legend to the plot
legend("topleft", legend=c("Doctor", "0.5mg Ranibizumab", 
                           "0.3mg Ranibizumab"),
       col=c("orange", "skyblue", "gray", "darkblue"), 
       lty = 1:2, cex=0.8)
dev.off()
drive_upload("/Users/charlesoneill/Documents/Macuject/Drive_API/anchor_plot.pdf",
             path = paste(drive_path, "anchor_plot.csv"))

