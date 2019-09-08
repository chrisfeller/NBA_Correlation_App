# Imports
library(shiny)
library(tidyverse)
library(ggplot2)
library(ggthemes)
library(DT)

# Set Working Directory
setwd('/Users/chrisfeller/Desktop/NBA_Corretion_App/app/')

# Read in correlation data 
total <- read.csv('data/Basketball_Reference_Total_Correlations.csv')
season <- read.csv('data/Basketball_Reference_Season_Correlations.csv')

ui <- fluidPage(
  titlePanel('NBA Correlation App'), 
  
  fluidRow(
  
  column(6, 
         h3('Correlation Table'),
         DT::dataTableOutput('table')),
  
  column(6, 
         selectInput("select", h3("Select Statistic"),
                     choices = sort(total$STATISTIC), selected = '%ASTD_2P'),
         helpText('Select a statistic to display over time.'), 
         br(), 
         plotOutput("plot"))
))
  
  

  

server <- function(input, output){
  output$table <- DT::renderDataTable(
    total[, c(1, 2, 4, 8)], options = list(lengthChange = FALSE,
                                           pageLength = 20, 
                                           searching = FALSE)) 
  
  selected <- reactive(season %>% filter(STATISTIC == input$select))
 

  output$plot <- renderPlot({
    selected() %>%
      ggplot(aes(x=SEASON, y=AVERAGE_RANK, group=1)) +
      geom_line() +
      geom_point() +
      labs(y = "Average Rank", x = 'Season') +
      ggtitle(sprintf("%s Correlation Over Time", input$select)) + 
      ylim(low=0, high=120) +
      theme_grey(15) + 
      theme(axis.text.x = element_text(angle = 45, hjust = 1), 
            plot.title = element_text(hjust = 0.5, face = 'bold'))
      # scale_color_fivethirtyeight() +
      # theme_fivethirtyeight()
    
  })
}

shinyApp(ui = ui, server = server)