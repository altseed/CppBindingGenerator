class WrapperGenerator(object):
    def __init__(self):
        self.definition:Definition = None
        self.output_path:str = ''
        self.header:str = ''
        self.shared_ptr_creator_name:str = 'CreateAndAddSharedPtr'
        self.shared_ptr_creator_name_dependence:str = 'CreateAndAddSharedPtrDependence'
        self.shared_ptr_getter_name:str = 'AddAndGetSharedPtr'
        self.shared_ptr_getter_name_dependence:str = 'AddAndGetSharedPtrDependence'