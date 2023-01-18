def generate_table(rows, columns):
    # Create the colgroup
    colgroup = "<col style='width: 226.67px;'/><col style='width: 226.67px;'/><col style='width: 226.67px;'/>"

    # Create the table
    table = f"<table data-layout='default' ac:local-id='1f3518c4-e712-4df2-8720-e68fd37682d5'><colgroup>{colgroup}</colgroup>"
    table += "<tbody>"

    for i in range(rows+1):
        table += "<tr>"
        for j in range(columns):
            if i == 0:
                table += "<th><p></p></th>"
            else:
                table += "<td><p></p></td>"
        table += "</tr>"
    table += "</tbody></table>"
    return table

def generate_table_with_images(rows, columns, files, orientation, position):
    insert_at = int(position)
    file_names=[]
    for f in files:
        img = f.rsplit('/',1)[-1]
        file_names.append(img)
    print(file_names)

    # Create the colgroup
    colgroup = "<col style='width: 226.67px;'/><col style='width: 226.67px;'/><col style='width: 226.67px;'/>"

    # Create the table
    table = f"<table data-layout='default' ac:local-id='1f3518c4-e712-4df2-8720-e68fd37682d5'><colgroup>{colgroup}</colgroup>"
    table += "<tbody>"
    if orientation == "V":
        for i in range(1, rows):
            table += "<tr>"
            for j in range(columns):
                if j == insert_at - 1 and i < len(file_names)+1:
                    table += f"<td><p><ac:image ac:align='center' ac:layout='center' ac:original-height='400' ac:original-width='400'><ri:attachment ri:filename='{file_names[i-1]}' /></ac:image></p></td>"
                else:
                    table += "<td><p></p></td>"
            table += "</tr>"
    elif orientation == "H":
        for i in range(insert_at, rows + 1):
            table += "<tr>"
            for j in range(columns):
                if j < len(file_names) and i == insert_at:
                    table += f"<td><p><ac:image ac:align='center' ac:layout='ceLnter' ac:original-height='400' ac:original-width='400'><ri:attachment ri:filename='{file_names[j]}' /></ac:image></p></td>"
                else:
                    table += "<td><p></p></td>"
            table += "</tr>"
    table += "</tbody></table>"

      
    #print(table)
    return table