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

Finish# AP Stats Final Project
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

Finish
