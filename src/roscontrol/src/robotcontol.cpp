#include "roscontroller.h"
#include "rosharwareinterface.h"
#include <controller_interface/controller.h>
#include <controller_manager.h>
main()
{
  MyRobot robot;
  controller_manager::ControllerManager cm(&robot);

  while (true)
  {
     robot.read();
     cm.update(robot.get_time(), robot.get_period());
     robot.write();
     sleep();
  }
}