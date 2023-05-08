import subprocess

spiders = ['jumia_kenya', 'jumia_nigeria', 'jumia_uganda', 
           'jumia_morocco', 'jumia_algeria', 'jumia_tunisia', 
            'jumia_coteivoire', 'jumia_senegal']

processes = []
for spider in spiders:
    cmd = ['scrapy', 'crawl', spider]
    process = subprocess.Popen(cmd)
    processes.append(process)
    
for process in processes:
    process.wait()