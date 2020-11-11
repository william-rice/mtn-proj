from selenium import webdriver
from selenium.webdriver.support.ui import Select

# Use Chrome as our choice of browser
# Go make sure you have google chromedriver installed in user/local/bin
# In the selenium docs, 7.21 WebElement is a useful section to read
driver = webdriver.Chrome()

# Open Mtn Proj website
driver.get('https://www.mountainproject.com/')
assert "Mountain Project" in driver.title

# Set type of route
type = driver.find_element_by_id("type")
Select(type).select_by_visible_text("Rock")

# Set minimum difficulty
diffMinrock = driver.find_element_by_id("diffMinrock")
Select(diffMinrock).select_by_visible_text("5.7")

all_options = diffMinrock.find_elements_by_tag_name("option")
for option in all_options:
    if option.is_selected():
        print("{} is selected".format(option.text))

# Set maximum difficulty
diffMaxrock = driver.find_element_by_id("diffMaxrock")
Select(diffMaxrock).select_by_visible_text("5.15d")

all_options = diffMaxrock.find_elements_by_tag_name("option")
for option in all_options:
    if option.is_selected():
        print("{} is selected".format(option.text))

# You can filter further if the need arises

# Click "Change" to change area
routeFinderForm = driver.find_element_by_id("routeFinderForm")
routeFinderForm.find_element_by_link_text("Change").click()

# Select the area
driver.implicitly_wait(5) # Because the dialog box takes time to load
area_list_element = driver.find_element_by_id("area-list")
areas = area_list_element.find_elements_by_xpath(".//a")
for area in areas:
    print(area.get_attribute("data-area-title"))
    area.click()
    submit_area = driver.find_element_by_id("select-area")
    submit_area.click()
    routeFinderForm.submit()
    results_summary = driver.find_element_by_class_name("float-md-left")
    print(results_summary.text)
    #To do: read the last number in the text
    #that appears before "Change Settings"
    driver.close()
driver.close()
