#Python 3.10.0

from cryptography.hazmat.primitives import hashes
from collections import Counter
import re, json, random
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statistics
from math import sqrt

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
    for x in range(0, len(pos_to_remove) -1):
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
#left in for legacy reasons
def make_blox_plot(list: list, show= False, download= False, path_to_save_to:str =  "", id =""):
    if show == False and download == False:
        #Dont waste time generating a graph that is not used
        pass
    else: 
        data = {
            "Shakespeare": list[0],
            "Modern": list[1]
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

#Make Barplot (more useful)
def make_bar_plot(inp_list: list, path_to_save_to: str, name: str):
    print(list)
    inp_list = [sorted(dict(inp_list[0]).items()), sorted(dict(inp_list[1]).items())]
    list_1_keys = list(dict(inp_list[0]).keys())
    list_2_keys = list(dict(inp_list[1]).keys())
    list_1_vals = list(dict(inp_list[0]).values())
    list_2_vals = list(dict(inp_list[1]).values())
    fig, axs = plt.subplots(1, 2)
    axs[0].legend(title="Shakespeare")
    axs[1].legend(title="Modern")
    sns.barplot(x= list_1_keys, y= list_1_vals, ax=axs[0])
    sns.barplot(x= list_2_keys, y= list_2_vals, ax=axs[1])
    fig.tight_layout()
    fig.savefig(f"{path_to_save_to}/{name}")

def confidence_interval(two_way_table: list, z_score: int = 1.645):
    condence_array = []
    for x in range(0, len(two_way_table[0])):
        condence_array.append(two_way_table[0][x])
        condence_array.append(two_way_table[1][x])
    mean = (sum(two_way_table[0]) / len(two_way_table[0])) + (sum(two_way_table[1]) / len(two_way_table[1]))
    sd = statistics.stdev(condence_array)
    lower_bound = mean - (z_score * (sd / sqrt(len(two_way_table[0]) * 2)))
    upper_bound = mean + (z_score * (sd / sqrt(len(two_way_table[0]) * 2)))
    return [lower_bound, upper_bound]

def updated_driver(sample_size, graph_name, redirect_output):
    reject = False
    
    #book1.txt --> Shakespeare
    #book2.txt --> Modern

    #Get the dictionary counts as counter objs
    counts_1 = file_reader("book1.txt", sample_size)["Counts"]
    counts_2 = file_reader("book2.txt", sample_size)["Counts"]

    #Fashion them into just the frequency lists
    counts_1_item = list(dict(counts_1).values())
    counts_2_item = list(dict(counts_2).values())

    #Form a Confidence Interval
    #Ask for help interpriting cause I have no idea what I just found
    conf_int = confidence_interval([counts_1_item, counts_2_item])

    #Voodoo magic
    curent_output = chi_square_for_independence(dict(counts_1), dict(counts_2))

    #Interprit the voodoo signs to tell the future
    if curent_output == "Invalid":
        print("Invalid")
    elif len(curent_output["exepts"]) == 0:
        if curent_output["chi_square"] < .05:
            #Reject the H0
            print(f"Reject the Null Hyp.\nTest Stat: {curent_output['chi_square']}\nConfidence Interval: {conf_int}")
            reject = True
        else:
            #F2R the H0
            print(f"Fail to reject the Null Hpt.\nTest Stat: {curent_output['chi_square']}\nConfidence Interval: {conf_int}")
    else:
        print("Failure of expected counts")

    #Output the raw data
    with open(redirect_output, "w") as file:
        json.dump({"freq": [dict(counts_1),
                            dict(counts_2)],
                            "test_stat": curent_output["chi_square"],
                            "dof": curent_output["dof"],
                            "conf_int":conf_int,
                            "reject": reject},
                            file, indent=4)

    #Print the commemritive photo of the voodoo magic
    #make_blox_plot([counts_1_item, counts_2_item], False, True, "Saves", graph_name)
    make_bar_plot([dict(counts_1), dict(counts_2)], "Saves", "VoodooPic.png")

#Run the new driver
updated_driver(3000, "VoodooPic", "summary.json")

#Depreciated
def driver():
    num_reject = 0
    num_fail = 0
    num_with_exeption = 0
    #stats_proj_base.txt -> passage

    #Dump_1 will be the old english
    #Dump_2 the modern

    #Run the sample one time
    for x in range(0, 1):
        #Generate the frequencies in pairs for even data
        counts_1 = file_reader("out.txt", 3000)["Counts"]
        counts_2 = file_reader("book2.txt", 3000)["Counts"]

        #Do the calculations and interprit the results
        curent_output = chi_square_for_independence(dict(counts_1), dict(counts_2))
        if curent_output != "Invalid":
            if len(curent_output["exepts"]) == 0:
                if curent_output["chi_square"] < .05:
                    num_reject += 1
                else:
                    num_fail += 1
            else:
                num_with_exeption +=1
        else: 
            print("Invalid")

    #End
    print(f"Number of times H0 was rejected: {num_reject}\nNumber of times H0 was accepted: {num_fail}\nNum of exep: {num_with_exeption}")
