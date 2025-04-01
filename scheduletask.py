from direct.task.TaskManagerGlobal import taskMgr


def scheduleTask( entity, method, extraArgs: list = None, appendTask = True, checkExisting = False ):
	name = f'{ entity.name }_{ method.__name__ }'
	if checkExisting:
		if taskMgr.hasTaskNamed( name ):
			return
	taskMgr.add( method, name = f'{ entity.name }_{ method.__name__ }', extraArgs = extraArgs, appendTask = appendTask )
