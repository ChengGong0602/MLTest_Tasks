import pandas as pd
import json

####### 0- Opening data files
# Opening JSON file
f = open('bbox_labels_600_hierarchy.json',)
data = json.load(f)  # returns JSON object as a dictionary
f.close()
labeled_data = data['Subcategory']

# read csv file
df = pd.read_csv('oidv6-class-descriptions.csv')
label_names = df["LabelName"]
class_names = df["DisplayName"]


def find_label_name(class_name):
    for i in range(0, len(class_names)):
        if class_name == class_names[i]:
            # print("index", label_names[i])
            return label_names[i]
    return None


def find_class_name(label_name):
    for i in range(0, len(label_names)):
        if label_name == label_names[i]:
            return class_names[i]
    return None


def flatten_json(nested_json):
    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out



def find_parent_name_from_flattenkey(flattenkey, flatten_json_result):
    parent_name = ""
    parent_key = ""
    split_name = flattenkey.split("_")[:-3]
    name_list_len = len(split_name)  
    for i in range(0, name_list_len):
        if i == name_list_len-1 and i == 0:
            parent_key = parent_key + split_name[i] + "_LabelName"
        else:
            if i==0:
                parent_key = parent_key + split_name[i]
            elif i<name_list_len-1:
                parent_key = parent_key + "_" + split_name[i]
            if i ==name_list_len-1:
                parent_key = parent_key + "_" + split_name[i] + "_LabelName"
    try:
        parent_label = flatten_json_result[parent_key]
        parent_name = find_class_name(parent_label)
    except Exception as error:
        print("error:", str(error))        
        pass                
    return parent_name        
    

def find_siblings_from_flatten_key(key, flatten_json_result):
    parent_name = ""
    splited_string = key.split("_")
    if len(splited_string)>2:
        siblings_list = []
        pairs = flatten_json_result. items()
        for pair_key, pair_value in pairs:         
            if pair_key.split("_")[:-2] == splited_string[:-2]:
                if parent_name=="": # find parent name only once
                    parent_name = find_parent_name_from_flattenkey( pair_key, flatten_json_result)
                matched_label_name = flatten_json_result[pair_key]
                matched_class_name = find_class_name(matched_label_name)
                siblings_list.append(matched_class_name)
        return {"parent_name": parent_name, "siblings_list": siblings_list}

    else:
        return None   


def find_parentclass_from_flatten_key(key, flatten_json_result):
    parent_name = ""
    splited_string = key.split("_")
    if len(splited_string) > 2:
        pairs = flatten_json_result. items()
        for pair_key, pair_value in pairs:
            if pair_key.split("_")[:-2] == splited_string[:-2]:
                if parent_name == "":  # find parent name only once
                    parent_name = find_parent_name_from_flattenkey(
                        pair_key, flatten_json_result)
        return parent_name

    else:
        return None
    

###### 1- Find all siblings class of a class name


def find_all_siblings(class_name):
    # class_name = "Doll"
    result = ""
    labeled_name = find_label_name(class_name)
    print("labeled_name", labeled_name)
    flatten_json_result = flatten_json(labeled_data)
    pairs = flatten_json_result. items()
    for key, value in pairs:
        # print(value)
        if value == labeled_name:
            print("key", key)
            result = find_siblings_from_flatten_key(key, flatten_json_result)
    return result
'''
class_name = "Crown"
print("find_all_siblings", find_all_siblings(class_name))
'''
###### 2-- Find the parent class of a class name


def find_parentclass_of_class(class_name):
    # class_name = "Doll"
    result = ""
    labeled_name = find_label_name(class_name)
    flatten_json_result = flatten_json(labeled_data)

    pairs = flatten_json_result. items()
    for key, value in pairs:
        # print(value)
        if value == labeled_name:
            result = find_parentclass_from_flatten_key(
                key, flatten_json_result)
    return result
'''
class_name = "Crown"
print("find_parentclass_of_class", find_parentclass_of_class(class_name))
'''

###### 3 Find all ancestor classes of a class name


def find_ancestor_from_class(class_name, count):     
    ancestor = []
    for i in range(0, count):
        class_name = find_parentclass_of_class(class_name)
        ancestor.append(class_name)        
    return ancestor


def find_all_ancestors(class_name):
    ''' This function will return ancestor class name list. 
        for example ex: 
        [parent class, 
        super class of parent class, 
        super class of super class of parent class, 
        ...class,
        top ancestor class
        ]
    '''
    ancestor = []
    labeled_name = find_label_name(class_name)
    flatten_json_result = flatten_json(labeled_data)

    pairs = flatten_json_result. items()
    for key, value in pairs:
        # print(value)
        if value == labeled_name:            
            splited_string = key.split("_")
            depth = int(len(splited_string)/2)           
            count = depth-1
            ancestor = find_ancestor_from_class(class_name, count)
            
    return ancestor      

'''
class_name = "Caterpillar"
print(find_all_ancestors("class_name"))
'''

###### 4 Find if both class 1 and class 2 belong to the same ancestor class(es)


def check_same_ancestors(class1, class2):
    ancestor_class1 = find_all_ancestors(class1)[-1]
    ancestor_class2 = find_all_ancestors(class2)[-1]
    if ancestor_class1 == ancestor_class2:
        return True
    else:
        return False
    
'''
class_name1 = "Insect"
class_name2 = "Caterpillar"
print(check_same_ancestors(class_name1, class_name2))
'''