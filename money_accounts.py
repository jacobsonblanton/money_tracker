# this app will implement the 50-30-20 rule when a user enters their paycheck amount.
# It takes the paycheck splits up where the money should go into. ( debt/savings - 20%, wants - 30%, needs - 50%)
# The user will have the option to allow the app to make the decision whether or not the item is a want or need. 

# (will add more later and as well as add a server and database implementation)


from money_tracker import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)