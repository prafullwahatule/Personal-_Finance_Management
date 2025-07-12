from django.urls import path
from . import views
from home.views import logout_user

urlpatterns = [
    path('', views.dashboard_home, name='dashboard'),  

    path('expense_logs_handler/', views.expense_logs_handler, name='expense_logs_handler'),


    # ✅ chat-boat URLs
    # path('gemini-chat/', views.gemini_chat_view, name='gemini_chat'),

    # ✅ project chat-boat URLs
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('api/get_user_first_name/', views.get_user_first_name, name='get_user_first_name'),


    # ✅ Stock URLs
    path('suggest_top_stocks_api/', views.suggest_top_stocks_api, name='suggest_top_stocks_api'),
    
    # ✅ Mutual Fund URLs
    path('api/suggest-top-mutual-funds/', views.suggest_top_mutual_funds_api, name='suggest_top_mutual_funds'),

    
    # Commodity ke liye (naya add karna hai)
    path('api/suggest_top_commodities/', views.suggest_top_commodities_api, name='suggest_top_commodities'),
    
    #cryptocurrency URLs
    path('suggest_top_cryptos_api/', views.suggest_top_cryptos_api, name='suggest_top_cryptos_api'),

    # ✅ compare for all stocks, mutual funds, commodities, and cryptocurrencies
    path('api/compare-assets/', views.compare_assets_api, name='compare_assets_api'),
  

    # this urls are dashboard income tracker history
    path('income-analysis/', views.income_analysis_view, name='income-analysis'),
    path('expense-analysis/', views.expense_analysis_view, name='expense-analysis'),
    path('combined-analysis/', views.combined_analysis_view, name='combined_analysis'),



    # ✅ expense tracker URLs
    path('expenses/', views.expense_tracker, name='expense_tracker'),
    path('expenses/add/', views.add_expense_view, name='add_expense'),
    path('manage-budget-limits/', views.manage_budget_limits, name='manage_budget_limits'),
    path('expense/delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('expenses/download/', views.download_expenses, name='download_expenses'),


    

    # Income Tracker
    path('income/', views.income_tracker, name='income_tracker'),
    path('income/delete/<int:income_id>/', views.delete_income, name='delete_income'),
    path('add-income/', views.add_income_view, name='add_income'),
    path('income/download/', views.download_income, name='download_income'),


    
    
    


    # ✅ Market Section URLs
    path('market/', views.market_update, name='market_update'),  # ✅ SIP Gainers & Losers
    path('api/market-indices/', views.get_market_indices, name='get_market_indices'),  # ✅ Market Indices
    path('get_index_chart/<str:index_name>/', views.get_index_chart, name='get_index_chart'),
    path('get_stock_highlights/', views.get_stock_highlights, name='get_stock_highlights'),
    path('api/top-gainers-losers/', views.get_top_gainers_losers, name='get_top_gainers_losers'),  # ✅ Top 5 Gainers & Losers
    path("get-economic-events/", views.get_economic_events, name="get-economic-events"),
    path('dashboard/download-economic-report/', views.download_economic_report, name='download_economic_report'),
    path('market/get_currency_commodities/', views.get_currency_commodities, name='get_currency_commodities'),
    path("get_news_updates/", views.get_news_updates, name="get_news_updates"),
    path('upcoming-ipos/', views.upcoming_ipos, name='upcoming_ipos'),
    
    

    # ✅ Settings URLs
    path('setting/', views.setting_view, name='setting_view'),
    path('manage-password/', views.manage_password_view, name='manage_password'),
    # path('delete-account/', views.delete_account_view, name='delete_account'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    path('request-delete-otp/', views.request_delete_otp, name='request_delete_otp'),
    path('verify-delete-otp/', views.verify_delete_otp, name='verify_delete_otp'),


    


    # ✅ Report URLs
    path('report', views.report_view, name='report'),
    path('generate-pdf-report/', views.generate_pdf_report, name='generate_pdf_report'),

    path('generate-csv-report/', views.generate_csv_report, name='generate_csv_report'),
    path('generate-excel-report/', views.generate_excel_report, name='generate_excel_report'),

    # ✅ logout URLs
    path('logout', logout_user, name='logout'),
    
]



