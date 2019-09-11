# Imports
library(shiny)
library(tidyverse)
library(ggplot2)
library(ggthemes)
library(DT)
library(shinythemes)
library(shinydashboard)

# Set Working Directory
setwd('/Users/chrisfeller/Desktop/NBA_Correlation_App/app/')

# Read in correlation data 
pearson <- read.csv('data/pearson_correlation.csv', check.names=FALSE)
spearman <- read.csv('data/spearman_correlation.csv', check.names=FALSE)
lags <- read.csv('data/Basketball_Reference_Season_Lags.csv', check.names=FALSE)
season <- read.csv('data/Basketball_Reference_Season_Correlations.csv', check.names=FALSE)

ui <- dashboardPage(skin = 'blue', 
  dashboardHeader(title = 'NBA Correlation App', titleWidth = 1700),
  
  dashboardSidebar(
    selectInput("statistic", h3("Statistic"),
                choices = sort(pearson$STATISTIC),
                selected = 'AVERAGE_AGE'),
    helpText('Select a statistic'), 
    selectInput('correlation', h3('Correlation Coefficient'),
                choices = c('Pearson Correlation', 'Spearman Correlation'),
                selected = 'Pearson Correlation'),
    helpText('Select a correlation')
  ),
  
  dashboardBody(
  fluidRow(
  column(3,
         h3('Correlation Table'),
         DT::dataTableOutput('table')), 
  
  column(9,
         h3('Plots'),
         br(),
         br(),
         plotOutput("plot"), 
         br(), 
         plotOutput("plot2"))
  
)))

server <- function(input, output){
  output$table <- DT::renderDataTable(
    
    if (input$correlation == 'Pearson Correlation') {
    pearson %>% 
        select('STATISTIC', input$statistic) %>% 
        arrange(desc(abs(pearson[[sprintf('%s', input$statistic)]]))) }
    
    else if (input$correlation == 'Spearman Correlation') {
      spearman %>% 
        select('STATISTIC', input$statistic) %>% 
        arrange(desc(abs(spearman[[sprintf('%s', input$statistic)]]))) },  
    
    options = list(lengthChange = FALSE,
                   pageLength = 20, 
                   searching = FALSE))
  
  
  output$plot <- renderPlot({
    if (input$correlation =='Pearson Correlation') {
    lags %>%
      ggplot(aes_string(x=paste0("`", input$statistic, "`"), 
                        y=sprintf('`%s_lag`', input$statistic))) +
      geom_point() +
      labs(y = "N Year Value", x = 'N+1 Year Value') +
      ggtitle(sprintf('Season Over Season Correlation: %s', round(cor(lags[input$statistic], lags[sprintf('%s_lag', input$statistic)], method = 'pearson'), 3))) +
      theme(plot.title = element_text(hjust = 0.5, face = 'bold')) }
    
    else if (input$correlation =='Spearman Correlation') {
      lags %>%
        ggplot(aes_string(x=paste0("`", input$statistic, "`"), 
                          y=sprintf('`%s_lag`', input$statistic))) +
        geom_point() +
        labs(y = "N Year Value", x = 'N+1 Year Value') +
        ggtitle(sprintf('Season Over Season Correlation: %s', round(cor(lags[input$statistic], lags[sprintf('%s_lag', input$statistic)], method = 'spearman'), 3))) +
        theme(plot.title = element_text(hjust = 0.5, face = 'bold')) }
    
      }
    )
  
  selected <- reactive(season %>% filter(STATISTIC == input$statistic))
  
  output$plot2 <- renderPlot({
    if (input$correlation == 'Pearson Correlation') {
      selected() %>%
        ggplot(aes(x=SEASON, y=PEARSON_CORRELATION, group=1)) +
        geom_line() +
        geom_point() +
        labs(y = "Pearson Correlation", x = 'Season') +
        ggtitle("Correlation with Net Rating Over Time") + 
        ylim(low=-1, high=1) +
        theme_grey(15) + 
        theme(axis.text.x = element_text(angle = 45, hjust = 1), 
              plot.title = element_text(hjust = 0.5, face = 'bold'))}
    
    else if (input$correlation == 'Spearman Correlation') {
      selected() %>%
        ggplot(aes(x=SEASON, y=SPEARMAN_CORRELATION, group=1)) +
        geom_line() +
        geom_point() +
        labs(y = "Spearman Correlation", x = 'Season') +
        ggtitle("Correlation with Net Rating Over Time") + 
        ylim(low=-1, high=1) +
        theme_grey(15) + 
        theme(axis.text.x = element_text(angle = 45, hjust = 1), 
              plot.title = element_text(hjust = 0.5, face = 'bold'))
    }
    
  })
  
  }

shinyApp(ui = ui, server = server)
