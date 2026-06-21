<h1>Analysis Process</h1>

<p>The analysis followed a structured data analytics workflow consisting of data preparation, exploratory analysis, descriptive analysis, and diagnostic analysis.</p>

<h2>Data Preparation and Quality Assessment</h2>
<p>Before conducting any analysis, the dataset was inspected and cleaned using Python and Pandas.
The following quality checks were performed:</P>

<h2>Data loading and inspection</h2>
<ol>
<li>Loaded the CSV dataset into a Pandas Data Frame.</li>
<li>Reviewed the dataset structure.</li>
<li>Checked the number of rows and columns.</li> 
<li>Examined column names and data types.</li>
</ol>

<h2>Missing values assessment</h2>
<ol>
<li>Checked all columns for missing values.</li>
<li>No missing values were identified; therefore, no imputation or removal was required.</li>
</ol>

<h2>Duplicates assessment</h2>
<ol>
<li>Checked for duplicate records to prevent double counting of sales.</li>
<li>No duplicate records were found; therefore, no records were removed.</li>
</ol>

<h2>Date preparation</h2>
<ol>
<li>Converted Order Date and Ship Date into datetime format.</li>
<li>Ensured date fields were suitable for yearly and monthly sales trend analysis.</li>
</ol>

<h2>Database creation</h2>
<ol>
<li>After data validation, the cleaned dataset was stored in SQLite.</li>
<li>The dataset was imported into a table named superstore, allowing SQL to be used for all analytical investigations.</li>
</ol>

<h2>Analytical approach</h2>
<p>The project was conducted in two major stages:</p>
<h2>Stage 1: Exploratory and descriptive analysis</h2>
<P>The objective was to understand what happened within the business by examining overall sales performance, regional performance, customer behaviour, product performance, and sales trends.</p>
<h2>Stage 2: Diagnostic analysis</h2>
<p>The objective was to identify the reasons behind the South region's underperformance by comparing it with the higher-performing West and East regions.</p>
