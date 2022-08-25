from datetime import datetime
import re
import time
from . import hashWork
from django.shortcuts import render, redirect
from pathlib import Path
from django.http import HttpResponseRedirect
import os
import stat


filesToBeDeleted = dict()


def showErrorsView(request):
    if request.method == "POST":
        if "to-main" in request.POST:
            return redirect("main")
        elif "delete-file" in request.POST:
            pth = Path("delete_errors.txt")
            if pth.exists():
                pth.unlink()
            else:
                # if cheeky user deleted the file in the meantime, simply go back to main site
                pass
            return redirect("main")

    with open("delete_errors.txt", 'r', encoding='utf-16') as file:
        issueFiles = file.readlines()
    errorFilesContext = {
        'issues': issueFiles
    }
    return render(request, 'dups/view_file.html', errorFilesContext)


def deleteView(request):
    numberDeleted = request.GET['howMany']
    if request.method == "POST":
        if "to-main" in request.POST:
            return redirect("main")
        elif "view-errors" in request.POST:
            return redirect("show-errors")
    return render(request, 'dups/delete.html', {'howMany': numberDeleted})


def listingView(request):
    if request.method == "GET":
        global filesToBeDeleted
        start_time = time.perf_counter()
        paths = request.GET['paths'].split("*")
        filesList = hashWork.getHash(paths[0], paths[1])
        finish_time = time.perf_counter()
        duration = f"{finish_time - start_time:.2f} seconds"
        dupedFiles = 0
        for _, y in filesList.items():
            dupedFiles += len(y)

        filesContext = {
            'files': filesList,
            'count': len(filesList),
            'duration': duration,
            'dupedFiles': dupedFiles,
        }
        filesToBeDeleted = filesList

    if request.method == "POST":
        counter, issues = 0, False
        for _, y in filesToBeDeleted.items():
            for file in y:
                try:
                    Path(file).unlink()
                    counter += 1
                except (FileExistsError, FileNotFoundError):
                    with open("delete_errors.txt", 'a', encoding='utf-16') as err_file:
                        if issues == False:
                            date_now = datetime.now().strftime("%d/%m/%Y at: %H:%M:%S")
                            err_file.write(
                                f"\n\n=== File generated on '{date_now}' ===\n\n\tCouldn't delete the following files (do they still exist?):\n")
                        err_file.write(str(file)+"\n")
                    issues = True
                except PermissionError:
                    os.chmod(file, stat.S_IWRITE)
                    Path(file).unlink()
                    counter += 1

        filesToBeDeleted = dict()
        file_err = str(Path().cwd())+"\\delete_errors.txt"

        return HttpResponseRedirect(f"/delete/?howMany={counter}&issues={issues}&file_err={file_err}")

    return render(request, 'dups/listing.html', filesContext)


def inspect_path(a, b):
    # lazy evaluation - no point checking further if previous condition not met
    result = []
    # result[0] - status
    # result[1] - comment

    if a == b:
        result.append(False)
        result.append("Paths given are the same.")
        return result
    if a == "" or b == "":
        result.append(False)
        result.append("At least one path not specified")
        return result
    if (not Path(a).exists()) or (not Path(b).exists()):
        result.append(False)
        result.append("At least one of the paths is NOT valid")
        return result

    # is one subdir of the other
    if (Path(a) in Path(b).parents) or Path(b) in Path(a).parents:
        result.append(False)
        result.append("One path is a subdirectory of another")
        return result

    result.append(True)
    result.append("OK, comparison possible.")
    return result


def mainView(request):
    return render(request, 'dups/main.html')


def statusView(request):
    userGiven = request.POST
    path_a = userGiven['first_path']
    path_b = userGiven['second_path']
    result = inspect_path(path_a, path_b)
    filesList = []

    contextData = {
        'result': result[0],
        'comment': result[1],
        'files': filesList,
    }

    # getting actual work done if result is 'True'
    if result[0]:
        # hashWork.getHash(path_a, path_b)
        return HttpResponseRedirect(f"/listing/?paths={path_a}*{path_b}")

    return render(request, 'dups/status.html', contextData)
