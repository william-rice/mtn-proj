import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# Use Chrome as our choice of browser
# Go make sure you have google chromedriver installed in user/local/bin
# In the selenium docs, 7.21 WebElement is a useful section to read
driver = webdriver.Chrome()
driver.implicitly_wait(5) # Because some things take time to load

# Open Mtn Proj website
driver.get('https://www.mountainproject.com/')
assert "Mountain Project" in driver.title

def set_search_settings(
        route_type="Rock",
        minimum_difficulty="5.7",
        maximum_difficulty="5.15d"):
    """
    Tells the driver to adjust the search parameters.

    args
    ----
    route_type (String: eg. "Rock")
    minimum_difficulty (String: eg. "5.7")
    maximum_difficulty (ditto)

    """
    # Set type of route
    type = driver.find_element_by_id("type")
    Select(type).select_by_visible_text(route_type)

    # Set minimum difficulty
    diffMinrock = driver.find_element_by_id("diffMinrock")
    Select(diffMinrock).select_by_visible_text(minimum_difficulty)

    all_options = diffMinrock.find_elements_by_tag_name("option")
    for option in all_options:
        if option.is_selected():
            print("{} is selected".format(option.text))

    # Set maximum difficulty
    diffMaxrock = driver.find_element_by_id("diffMaxrock")
    Select(diffMaxrock).select_by_visible_text(maximum_difficulty)

    all_options = diffMaxrock.find_elements_by_tag_name("option")
    for option in all_options:
        if option.is_selected():
            print("{} is selected".format(option.text))
set_search_settings()


def download_routes(current_level=1, current_area=None):
    # Click "Change" to change area (do this every time)
    routeFinderForm = driver.find_element_by_id("routeFinderForm")
    routeFinderForm.find_element_by_link_text("Change").click()
    print(current_level)
    if current_level > 1:
        current_area.click()

    # Select the area
    area_list_element = driver.find_element_by_id("area-list")
    areas = area_list_element.find_elements_by_xpath(".//a") # state links at level=0

    for area in areas:

        # ignore it if it's a level above:
        containing_div = area.find_element_by_xpath("..")
        link_level = containing_div.get_attribute("class")
        if int(re.search("\d",link_level).group()) != current_level:
            continue

        #print(area.get_attribute("data-area-title"))
        area.click()
        submit_area = driver.find_element_by_id("select-area")
        submit_area.click()
        routeFinderForm.submit()
        results_summary = driver.find_element_by_class_name("float-md-left")
        too_many_results = re.search("1000", results_summary.text)
        if too_many_results:
            # Go one level deeper
            driver.back()
            download_routes(current_level+1, area)
        else:
            print(area)

download_routes()
driver.close()
