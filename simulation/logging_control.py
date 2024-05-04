class EnhancedLoggingControl(LoggingControl):
    def _process_market_book(self, market_book):
        self.log(f"Market ID: {market_book.market_id} - Profit/Loss: {calculate_pnl(market_book)}")

framework.add_logging_control(EnhancedLoggingControl())
