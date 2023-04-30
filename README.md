# AP Stats Final Project
### File is ordered by the functions of the .py file and how they function
> This project uses a __Chi-Square test for independence__ to calculate letter frequency between modern and old English.

---

## Make Alpha
#### Accepts
>Non-nested <code>text</code>
#### Returns
>Sanitized <code>String</code>
#### Process
> -Iterate over input string and apply regex pattern to each letter

---

## File Reader
#### Accepts
> - file_name = "stats_proj_base.txt"
> - sample_size = 30
> - append_to_file = False
> - thread_id = None
#### Returns 
> <code> Dictionary </code>
> - Counts: Number of each letter in the selected sample
> - SSOW: Literal <code> List </code> of the words
#### Process
> - Open the file <code>file_name</code> and get random indice __i__ to __i + 1__
> - Combine the output of above
> - Sanitize with <code>make_alpha</code> 
> - Calculate letter frequencies
> > __IF__ the <code>append_to_file</code> arg is set
> > __THEN__ append to <code>dump_[thread_id]</code>

---

## Chi Square for Independence
#### Accepts
> Two <code>Dictionaries</code> of letters to frequencies
#### Returns
> - Chi Square: the X<sup>2</sup> test statistic
> - DoF: Degree of freedom
> - Exepts: <code>Dictionary</code> of failed expected counts of position to letter in <code>two_d_array</code>
> - Freq Array: The 2d array of frequencies used in the table
#### Process
> - Fill in any missing letters with a zero so that each <code>Dictionary</code> is the same length
> - Organize the elements of the arrays alphabetically
> - Remove the <code>Keys</code> from the arrays since letters can now be assumed by position and combine them into a 2d array
> - Eliminate every double zero and remove them from the list
> - Calculate the expected counts (EC)
> - Create a list of the ECs that are less than 5
> - Calculate the components of the test, Dof, and X<sup>2</sup> test stat

---

## Reformat Dump
#### Accepts
> <code>Int</code>
#### Process
> Reformat the corresponding dump file back to a blank <code>List</code>

---

## Make Box Plot
> Experimental graphing utility, not recommended for use
> Check code for uses if you really want to use it, otherwise
> it really isnt too useful

---

## Driver
##### Accepts
> None
#### Returns
> None
#### Process
> This is the driver code for the above processes and works to bridge them together
> Prints the formatted results to console 
