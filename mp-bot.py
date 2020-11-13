import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By

# Use Chrome as our choice of browser
# Go make sure you have google chromedriver installed in user/local/bin
# In the selenium docs, 7.21 WebElement is a useful section to read
driver = webdriver.Chrome()
driver.implicitly_wait(20) # Because some things take time to load

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

    # Set maximum difficulty
    diffMaxrock = driver.find_element_by_id("diffMaxrock")
    Select(diffMaxrock).select_by_visible_text(maximum_difficulty)

    all_options = diffMaxrock.find_elements_by_tag_name("option")

set_search_settings()

def get_element_from_list(link_elements, link_text):
    """
    Helper function for download_routes().

    Pulls out a specific area elements from a list of links.

    Returns current link (the one w/ link_text)
    and the next link in the list. This is a list of two items.

    OR

    Returns current link (just one item) if it's last in the list.
    """
    current_link = False

    for el in link_elements:
        if current_link: # false until next if statement executes
            next_link = el
            return [current_link, next_link]
        if el.get_attribute("data-area-title") == link_text:
            current_link = el

    if current_link:
        return current_link # if it's the last in the list, return just one

def download_routes(path=["International"]):
    print(path)

    # Click "Change" to open dialog window (do this every time)
    routeFinderForm = driver.find_element_by_id("routeFinderForm")
    routeFinderForm.find_element_by_link_text("Change").click()

    for area in path:
        # Get a list of the links in the window
        links_container = driver.find_element_by_id("area-list")
        links = links_container.find_elements_by_xpath(".//a")

        # Get the link for this area and the next (on this level)
        [current_link, next_sibling] = get_element_from_list(links,area) # defined above
        next_sibling_text = next_sibling.get_attribute("data-area-title")
        current_text = current_link.get_attribute("data-area-title")
        #print(cond.element_to_be_clickable(By.LINK_TEXT("International")))
        #WebDriverWait(driver,10).until(lambda x: x.find_element_by_link_text(current_text).element_to_be_clickable())
        current_link.click()
        if area != path[-1]:
            print("we continued")
            continue # go all the way down the path

        # Get the first child name for navigation
        new_links = links_container.find_elements_by_xpath(".//a")
        first_child_index = len(path)
        first_child = new_links[first_child_index]
        first_child_text = first_child.get_attribute("data-area-title")

        # Submit the form
        submit_area = driver.find_element_by_id("select-area")
        submit_area.click()
        routeFinderForm.submit()

        # Only download pages w/ results <1000
        results_summary = driver.find_element_by_class_name("float-md-left")
        too_many_results = re.search("1000", results_summary.text)

        if too_many_results:
            print("path had too many results")
            # Go one level deeper
            path.append(first_child_text)
            driver.back()
            download_routes(path)
        else:
            print("downloaded path") # this means download for now
            path.pop()
            path.append(next_sibling_text)
            driver.back()
            download_routes(path)

download_routes()
driver.close()
