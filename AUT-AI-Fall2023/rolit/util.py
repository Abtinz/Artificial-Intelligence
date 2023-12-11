import inspect
import sys
import pygame
import os

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" %
          (method, line, fileName))
    sys.exit(1)

def load_images(transforms=[]):
      image_dict = {}
      colors = set()

      for root, dirs, files in os.walk("images"):
            if len(files) == 0:
                  continue
            path = root.split(os.sep)
            colors.add(path[1])
            key = '_'.join(path[1:])
            if key not in image_dict:
                  image_dict[key] = []
            
            sorted_files = sorted(files)
            for file in sorted_files:
                  file_path = os.path.join(root, file)
                  image = pygame.image.load(file_path)
                  for transform in transforms:
                        image = transform(image)
                  image_dict[key].append(image)
      
      return image_dict, list(colors)

def lookup(name, namespace):
    """
    Get a method or class from any imported module from its name.
    Usage: lookup(functionName, globals())
    """
    dots = name.count('.')
    if dots > 0:
        moduleName, objName = '.'.join(
            name.split('.')[:-1]), name.split('.')[-1]
        module = __import__(moduleName)
        return getattr(module, objName)
    else:
        modules = [obj for obj in list(namespace.values()) if str(
            type(obj)) == "<type 'module'>"]
        options = [getattr(module, name)
                   for module in modules if name in dir(module)]
        options += [obj[1]
                    for obj in list(namespace.items()) if obj[0] == name]
        if len(options) == 1:
            return options[0]
        if len(options) > 1:
            raise Exception('Name conflict for %s')
        raise Exception('%s not found as a method or class' % name)
            

def load_modes(filename):
    """
    load the dictionary for different types of game configurations which are saved in a file
    """
    import pickle
    import os

    if not os.path.exists(filename):
        return None
    
    with open(filename, 'rb') as f:
        modes = pickle.load(f)

    return modes

