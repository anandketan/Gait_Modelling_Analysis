import pickle


with open('initial3d_by_mean.pkl', 'rb') as file:
    dicto = pickle.load(file)

print("This is the dict:", dicto)