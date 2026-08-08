# to test our files
from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from backend import run_travel_agent



# Test -01
# res = tavily_search("Best hotels in India")
# print(res)

# Test -02
# res = search_flights("Plan a 7 days Dubai trip from India" )
# print(res)

# Test - -03
user_input = input("Enter travel support : ")

response = run_travel_agent(
    user_input=user_input,
    thread_id="test_user"
)

print("\n FINAL RESPONSE : \n")
print(response["answer"])