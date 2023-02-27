<h1>Personal Book Analysis on GCP</h1>

<p>This project concerns the ingestion of my personal books in Amazon into GCP for data analysis. The goal is to compare my personal book data with 3 Kaggle datasets related to books, and to demonstrate good data engineering practices such as using multiprocessing programming, metadata creation, and data source tracking. The analysis will provide insights into my personal book taste compared to Amazon bestsellers and other book datasets.</p>

<h2>Data Sources</h2>

<ul>
    <li>Personal book data from Amazon</li>
    <li>Kaggle datasets:
        <ul>
            <li>Bestsellers</li>
            <li>Goodreads books</li>
            <li>50,000+ Books</li>
        </ul>
    </li>
</ul>

<h2>Project Structure</h2>

<p>The project is structured as follows:</p>

<ul>
    <li><code>data_ingestion</code> folder: contains scripts for data ingestion</li>
    <li><code>data_analysis</code> folder: contains scripts for data analysis</li>
    <li><code>metadata</code> folder: contains metadata files for each dataset</li>
    <li><code>results</code> folder: contains analysis results</li>
</ul>

<h2>Data Ingestion</h2>

<p>Data ingestion is done using GCP services such as Cloud Storage and BigQuery. Each dataset has its own metadata file in the <code>metadata</code> folder, which tracks the source of the data and any other relevant information.</p>

<h2>Data Analysis</h2>

<p>Data analysis is done using Python scripts in the <code>data_analysis</code> folder. The analysis includes comparing my personal book data with the Kaggle datasets, exploring trends and patterns in the data, and generating visualizations to aid in understanding the data.</p>

<h2>Conclusion</h2>

<p>This project demonstrates good data engineering practices such as using multiprocessing programming, metadata creation, and data source tracking. The analysis provides insights into my personal book taste compared to Amazon bestsellers and other book datasets. The results of the analysis can be found in the <code>results</code> folder.</p>
