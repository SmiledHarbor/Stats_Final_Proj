#Python 3.10.0

from cryptography.hazmat.primitives import hashes
from collections import Counter
import re, json, random
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#A "Simple" script to calculate the Chi-square test statistic between the letter
#frequencies in modern English vs. old English.
#The texts are downloaded from the Gutenberg project in the UTF-8 format
#https://www.gutenberg.org/
#Visit the README for more info on project details

def make_alpha(inp):
    #Init char list
    alpha = []

    #Init regex pattern
    pattern = re.compile("^[a-zA-Z]+$")

    #Extract letters
    for letter in str(inp):
        if pattern.match(str(letter)):
            alpha.append(str(letter))

    return str("".join(alpha)).lower().strip()

#Opens the base file and removes [sample_size] number of words
#consecutivly. Then sterilizes them to letters only and counts the 
#amount of each letter. 
#To use the append option, a unique ID must be provided for thread-safty
def file_reader(file_name = "stats_proj_base.txt", sample_size = 30, append_to_file = False, thread_id = None):
    sample_size_of_words = []

    #Open the file
    with open (file_name, "r", encoding="utf-8") as file:

        #The the text as-is
        full_text = file.read()

        #Split the text by the sace
        words = full_text.split(" ")

        #Create a random indecy less than sample_size
        #Default sample size is 30 for Cen. lim. Theorm
        rand = random.randint(0, len(words) - sample_size)
        
        #Append the samle size of words to respective list
        for i in range(rand, rand + sample_size):
            sample_size_of_words.append(words[i])

    #Combine the output
    combined = "".join(sample_size_of_words)

    #Remove all nonletters
    stripped = make_alpha(combined)

    #Tally the letters
    counts = Counter(stripped)
    
    #Check to see if its supposed to write
    if append_to_file:

        #Make sure there is a ID attached
        if thread_id == None:
            raise Exception("Requires a THREAD_ID for thread-safe file appending")
        
        #Main body
        else:
            generic_obj = []

            #Open the JSON file and load the contentes
            with open(f"dump_{thread_id}.json", "r", encoding="uft-8") as file:
                generic_obj = json.load(file)
                generic_obj.append([counts])
            file.close()

            #Dump them back in with the new content appended and styled
            with open(f"dump_{thread_id}.json", "w") as file:
                json.dump(generic_obj, file, indent=4)
            file.close()
    #End
    return {"Counts": counts, "SSoW": sample_size_of_words}

#Does what it sounds like
def chi_square_for_independence(old_obj: dict, modern_obj: dict):

    #Yes I took this from the internet, I cant be asked to write this thing out
    WOW_ITS_THE_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    #Format the dicts into a 2 way table (2d array)
    #Since not every letter will be used, slap a zero in the blanks
    #by running the alphabet over the dump and finding discrepencies
    for letter in WOW_ITS_THE_ALPHABET:
        if letter not in old_obj:
            old_obj[letter] = 0
        if letter not in modern_obj:
            modern_obj[letter] = 0

    #Make the dicts, well, alphebetical
    sorted_old = sorted(old_obj.items())
    sorted_m = sorted(modern_obj.items())

    #Now that they are alphabetical, the keys can be assumed by their pos in WOW_ITS_THE_ALPHABET
    #so fashion them into two arrays of just frequencies
    old_freq = []
    m_freq = []
    for i in range(0, 26):
        old_freq.append(sorted_old[i][1])
        m_freq.append(sorted_m[i][1])
    
    #And FINALLY we can format it into a 2d array
    two_d_array = [old_freq, m_freq]

    #Note any double zeros and omitt them
    #This is because a double zero will raise a divide by zero error
    #on the calculator and a zero internal list val error in py
    double_zeros = {}
    pos_to_remove = []
    for x in range(0, len(two_d_array[0])):
        if two_d_array[0][x] == 0 and two_d_array[1][x] == 0:
            double_zeros[x] = WOW_ITS_THE_ALPHABET[x]
            pos_to_remove.append(x)
    for x in range(0, len(pos_to_remove)):
        del two_d_array[0][pos_to_remove[x]]
        del two_d_array[1][pos_to_remove[x]]

    #Tabulate row sums
    total_top = sum(two_d_array[0])
    total_bottom = sum(two_d_array[1])
    total_combine = total_bottom + total_top

    #Column totals
    column_totals = []
    for x in range(0, len(two_d_array[0])):
        column_totals.append(two_d_array[0][x] + two_d_array[1][x])
    
    #Expected values
    top_row_expected_values = []
    bottom_row_expected_values = []
    for x in range(0, len(column_totals)):
        #Top
        top_row_expected_values.append((total_top * column_totals[x]) / total_combine)

        #Bottom
        bottom_row_expected_values.append((total_bottom * column_totals[x]) / total_combine)
    expected_values = [top_row_expected_values, bottom_row_expected_values]

    #Make sure all expected values are proper size
    exeptions = []
    for x in range(0, len(expected_values[0])):
        if expected_values[0][x] < 5 or expected_values[1][x] < 5:
            exeptions.append({x: [WOW_ITS_THE_ALPHABET[x], f"NonFatal exeption at pos {x + 1}\n└> {expected_values[0][x]} or {expected_values[1][x]}"]})

    #Tablulate componenets
    #(O-E)^2 / E = x^2
    #O = Observed
    #E = Expected
    comps = []
    try:
        for x in range(0, len(expected_values[0])):
            comps.append(pow(two_d_array[0][x] - expected_values[0][x], 2) / expected_values[0][x])
            comps.append(pow(two_d_array[1][x] - expected_values[1][x], 2) / expected_values[1][x])
    except ZeroDivisionError:
        print(f"Zero in expected counts")
        return "Invalid"

    #Compile the componenets into X² test stat
    chi_square_test_stat = sum(comps)

    #Degree of Freedom
    degree_of_freedom = len(expected_values[0]) -1

    #Finalize the results and return them
    return {"chi_square": chi_square_test_stat, "dof": degree_of_freedom, "exepts": exeptions, "freq_array":two_d_array}

#Clear a dump file back to a blank list
def reformat_dump(num: int):
    with open(f"dump_{num}.json", "w") as file:
        file.flush()
        json.dump([], file)
    file.close()

#Make an SNS double boxplot of the data
#with the option to either save the fig or display
def make_blox_plot(list: list, show= False, download= False, path_to_save_to:str =  "", id =""):
    if show == False and download == False:
        #Dont waste time generating a graph that is not used
        pass
    else: 
        data = {
            "List 1": list[0],
            "List 2": list[1]
        }
        df = pd.DataFrame(data)
        sns.boxplot(data=df)
        if show:
            plt.show()
        if download:
            if path_to_save_to == "" or id=="":
                print(f"Nonfatal error in path: {path_to_save_to}: Path does not exist or is not subfolder")
            else: 
                plt.savefig(f"{path_to_save_to}/Trial_{id}.png")

def driver():
    num_reject = 0
    num_fail = 0
    num_with_exeption = 0
    #stats_proj_base.txt -> passage

    #Dump_1 will be the old english
    #Dump_2 the modern

    for x in range(0, 10000):
        #Generate the frequencies in pairs for even data
        counts_1 = file_reader("out.txt", 3000)["Counts"]
        counts_2 = file_reader("book2.txt", 3000)["Counts"]

        #Do the calculations and interprit the results
        curent_output = chi_square_for_independence(dict(counts_1), dict(counts_2))
        if curent_output != "Invlaid" and len(curent_output["exepts"]) == 0:
            if curent_output["chi_square"] < .05:
                num_reject += 1
            else:
                num_fail += 1
        else:
            num_with_exeption +=1

    #End
    print(f"Number of times H0 was rejected: {num_reject}\nNumber of times H0 was accepted: {num_fail}\nNum of exep: {num_with_exeption}")

    #There is always an exeption in the Expected Values being less than 5,
    #gotta check that out and find out how to fix it
    #Probably just adding more to the sample size
    #Ight got it
    #But still never rejected the H0 once <-- Duh, the sames came from the same text. Ofc they share letter frequencies
    # ^No I was right, it was just taking the same sample many times
    #
    #H0: There is no difference in letter frequency between the two samples
    #HA: There is a difference in the frequency between the two samples
    #
    #Use seaborn to make plots of the results (SNS)
    #https://stackoverflow.com/questions/44552489/plotting-multiple-boxplots-in-seaborn
#make_blox_plot([[12,23,45,25,64,25,85,23,57],[23,76,34,77,43,67,53,78,53]], True, False)
driver()