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
                choices = sort(pearson$STATISTIC)[sort(pearson$STATISTIC) != 'RANK'],
                selected = 'AVERAGE_AGE'),
    selectInput('correlation', h3('Correlation'),
                choices = c('Pearson', 'Spearman'),
                selected = 'Pearson'),
    br(), br(), br(), br(), br(), br(), 
    br(), br(), br(), br(), br(), br(), 
    br(), br(), br(), br(), br(), br(), 
    br(), br(), br(), br(), br(), br(), 
    br(), br(), br(), br(),
    HTML('<footer>
          <div align="center">
          <p>Chris Feller | chrisjfeller.com<p/>
         </div>
         </footer>')
  ),
  
  dashboardBody(
  fluidRow(
  column(3,
         DT::dataTableOutput('table')), 
  
  column(9,
         br(),
         br(),
         plotOutput("plot"), 
         br(), 
         plotOutput("plot2"))
  
)))

server <- function(input, output){
  output$table <- DT::renderDataTable(
    
    if (input$correlation == 'Pearson') {
    pearson %>% 
        mutate_if(is.numeric, ~round(., 3)) %>%
        select('STATISTIC', input$statistic) %>% 
        rename('CORRELATION' = input$statistic) %>%
        filter((STATISTIC != input$statistic) & (STATISTIC != 'RANK'))%>%
        arrange(desc(abs(CORRELATION)))}
    
    else if (input$correlation == 'Spearman') {
      spearman %>% 
        mutate_if(is.numeric, ~round(., 3)) %>%
        select('STATISTIC', input$statistic) %>% 
        rename('CORRELATION' = input$statistic) %>%
        filter(STATISTIC != input$statistic) %>%
        arrange(desc(abs(CORRELATION)))},  
    
    options = list(lengthChange = FALSE,
                   pageLength = 20, 
                   searching = FALSE))  
  
  
  output$plot <- renderPlot({
    if (input$correlation =='Pearson') {
    lags %>%
      ggplot(aes_string(x=paste0("`", input$statistic, "`"), 
                        y=sprintf('`%s_lag`', input$statistic))) +
      geom_point() +
      labs(y = "N Year Value", x = 'N+1 Year Value') +
      ggtitle(sprintf('Season Over Season Correlation: %s', round(cor(lags[input$statistic], lags[sprintf('%s_lag', input$statistic)], method = 'pearson'), 3))) +
      theme_grey(15) + 
      theme(plot.title = element_text(hjust = 0.5, face = 'bold')) }
    
    else if (input$correlation =='Spearman') {
      lags %>%
        ggplot(aes_string(x=paste0("`", input$statistic, "`"), 
                          y=sprintf('`%s_lag`', input$statistic))) +
        geom_point() +
        labs(y = "N Year Value", x = 'N+1 Year Value') +
        ggtitle(sprintf('Season Over Season Correlation: %s', round(cor(lags[input$statistic], lags[sprintf('%s_lag', input$statistic)], method = 'spearman'), 3))) +
        theme_grey(15) + 
        theme(plot.title = element_text(hjust = 0.5, face = 'bold')) }
    
      }
    )
  
  selected <- reactive(season %>% filter(STATISTIC == input$statistic))
  
  output$plot2 <- renderPlot({
    if (input$correlation == 'Pearson') {
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
    
    else if (input$correlation == 'Spearman') {
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
