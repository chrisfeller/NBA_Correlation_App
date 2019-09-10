# Imports
library(shiny)
library(tidyverse)
library(ggplot2)
library(ggthemes)
library(DT)
library(shinythemes)

# Set Working Directory
setwd('/Users/chrisfeller/Desktop/NBA_Corretion_App/app/')

# Read in correlation data 
total <- read.csv('data/Basketball_Reference_Total_Correlations.csv')
season <- read.csv('data/Basketball_Reference_Season_Correlations.csv')
lags <- read.csv('data/Basketball_Reference_Season_Lags.csv', check.names=FALSE)
                 
ui <- fluidPage(
  theme = shinytheme("yeti"),
  
fluidRow(
  column(12,offset = 4, titlePanel("NBA Correlation App")) 
), 

fluidRow(

column(6,
       h3('Correlation Table'),
       DT::dataTableOutput('table')),

column(6,
       selectInput("statistic", h3("Select Statistic"),
                   choices = sort(total$STATISTIC),
                   selected = '%ASTD_2P'),
       helpText('Select a statistic to plot'), 
       selectInput('plot_type', h3('Select Plot Type'),
                   choices = c('Average Rank', 'Pearson Correlation', 'Spearman Correlation'),
                   selected = 'Average Rank'),
       helpText('Select a plot type.'),
       plotOutput("plot"), 
       br(),
       plotOutput("plot2"))
))
  
  
server <- function(input, output){
  output$table <- DT::renderDataTable(
    total[, c(1, 2, 4, 8)], options = list(lengthChange = FALSE,
                                           pageLength = 20, 
                                           searching = FALSE)) 
  
  selected <- reactive(season %>% filter(STATISTIC == input$statistic))
  one <- reactive(lags %>% select(paste0("`", input$statistic, "`")))
  two <- reactive(lags %>% select(sprintf('`%s_lag`', input$statistic)))

  output$plot <- renderPlot({
    if (input$plot_type == 'Average Rank') {
      selected() %>%
        ggplot(aes(x=SEASON, y=AVERAGE_RANK, group=1)) +
        geom_line() +
        geom_point() +
        labs(y = "Average Rank", x = 'Season') +
        ggtitle("Correlation with W/L% Over Time") + 
        ylim(low=0, high=120) +
        theme_grey(15) + 
        theme(axis.text.x = element_text(angle = 45, hjust = 1), 
              plot.title = element_text(hjust = 0.5, face = 'bold')) }
    else if (input$plot_type == 'Pearson Correlation') {
      selected() %>%
      ggplot(aes(x=SEASON, y=PEARSON_CORRELATION, group=1)) +
      geom_line() +
      geom_point() +
      labs(y = "Pearson Correlation", x = 'Season') +
      ggtitle("Correlation with W/L% Over Time") + 
      ylim(low=-1, high=1) +
      theme_grey(15) + 
      theme(axis.text.x = element_text(angle = 45, hjust = 1), 
            plot.title = element_text(hjust = 0.5, face = 'bold'))}
    
    else if (input$plot_type == 'Spearman Correlation') {
      selected() %>%
        ggplot(aes(x=SEASON, y=SPEARMAN_CORRELATION, group=1)) +
        geom_line() +
        geom_point() +
        labs(y = "Spearman Correlation", x = 'Season') +
        ggtitle("Correlation with W/L% Over Time") + 
        ylim(low=-1, high=1) +
        theme_grey(15) + 
        theme(axis.text.x = element_text(angle = 45, hjust = 1), 
              plot.title = element_text(hjust = 0.5, face = 'bold'))
    }
      
  })
  
  output$plot2 <- renderPlot({
    lags %>%
      ggplot(aes_string(x=paste0("`", input$statistic, "`"), 
                        y=sprintf('`%s_lag`', input$statistic))) +
      geom_point() +
      labs(y = "N Year Value", x = 'N+1 Year Value') +
      ggtitle(sprintf('Season Over Season Correlation: %s', round(cor(lags[input$statistic], lags[sprintf('%s_lag', input$statistic)]), 3))) +
      theme(plot.title = element_text(hjust = 0.5, face = 'bold'))
    
    }
  )
}

shinyApp(ui = ui, server = server)