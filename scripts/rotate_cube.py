from __future__ import print_function
import vtk , sys , time
#sys.stdin = open('temp_data','r')
#f = open('temp_data', 'r', os.O_NONBLOCK)
f1 = open('temp_data' ,'r')
class vtkTimerCallback():
    def __init__(self):
        self.timer_count = 0

    def execute(self,obj,event):
       #print(self.timer_count)
       #self.actor.SetPosition(self.timer_count, self.timer_count,0);
        #print(str(pyperclip.paste()))
        ret_string = f1.readline().strip()
        if str(ret_string) == "Left Hand":
            self.actor.RotateX(1.0)

        if str(ret_string) == "Right Hand":
            self.actor.RotateX(-1.0)
        iren = obj
        iren.GetRenderWindow().Render()
        self.timer_count += 1
        time.sleep(0.1)

def main():
    #ColorBackground = [0.0, 0.0, 0.0]
    FirstobjPath = "table-mountain.obj"
    reader = vtk.vtkOBJReader()
    reader.SetFileName(FirstobjPath)
    reader.Update()

    colors = vtk.vtkNamedColors()
    # Set the background color.
    bkg = list(map(lambda x: x / 255.0, [26, 51, 102, 255]))
    colors.SetColor("BkgColor", *bkg)

    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(reader.GetOutput())
    else:
        mapper.SetInputConnection(reader.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    prop = actor.GetProperty()

    # Setup a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("Test")
    renderWindow.SetSize(600,600)
    renderWindow.AddRenderer(renderer);
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    #Add the actor to the scene
    renderer.AddActor(actor)
    renderer.SetBackground(0,0,0) # Background color black

    #Render and interact
    renderWindow.Render()

    # Initialize must be called prior to creating timer events.
    renderWindowInteractor.Initialize()

    # Sign up to receive TimerEvent
    cb = vtkTimerCallback()
    cb.actor = actor
    renderWindowInteractor.AddObserver('TimerEvent', cb.execute)
    timerId = renderWindowInteractor.CreateRepeatingTimer(100);

    #start the interaction and timer
    renderWindowInteractor.Start()


#if __name__ == '__main__':
#   main()
