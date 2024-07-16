const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

let inputDisposable; 
let input = ''; 
let startTime = new Date(); 
/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('Congratulations, your extension "Mohit" is now active!');

    let startDisposable = vscode.commands.registerCommand('Mohit.startRecording', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active text editor found.');
            return;
        }

        vscode.window.showInformationMessage('Recording started. Type your text and press Enter or ";" to log it.');

        inputDisposable = vscode.workspace.onDidChangeTextDocument(event => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                return;
            }
            const changes = event.contentChanges;
            if (changes.length) {
                const change = changes[0];
                console.log(change);
                
                if (change.text.includes(';') || change.text.includes('\n')) {
                    let endTime = new Date();
                    let timeTaken = (endTime.getTime() - startTime.getTime()) / 1000;
                    console.log(input, " - input");
                    writeCsv(input, startTime.toISOString(), endTime.toISOString(), timeTaken, change.text.includes('\n') == true ? "enter" : "semicolon");
                    input = ''; 
                    startTime = new Date();
                } else if (change.text === "" && change.rangeLength > 0) {
                    let endTime = new Date();
                    let timeTaken = (endTime.getTime() - startTime.getTime()) / 1000;
                    writeCsv(input, startTime.toISOString(), endTime.toISOString(), timeTaken, "backspace");
                    input = input.slice(0, -change.rangeLength);
                    console.log(input);
                } 
                else if (change.text != "" && change.rangeLength > 0) {
                    let endTime = new Date();
                    let timeTaken = (endTime.getTime() - startTime.getTime()) / 1000;
                    writeCsv(change.text, startTime.toISOString(), endTime.toISOString(), timeTaken, "suggestion");
                    console.log(input);
                } 
                else {
                    input += change.text;
                }
            }
        });

        context.subscriptions.push(inputDisposable);
    });

    let stopDisposable = vscode.commands.registerCommand('Mohit.stopRecording', function () {
        if (inputDisposable) {
            inputDisposable.dispose();
            vscode.window.showInformationMessage('Recording stopped.');
        } else {
            vscode.window.showInformationMessage('Recording is not active.');
        }
    });

    context.subscriptions.push(startDisposable, stopDisposable);
}


function writeCsv(text, startTime, endTime, timeTaken, event) {
    if (text === '') {
        console.log("empty");
        return;
    }

    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active text editor found.');
        return;
    }

    const currentFilePath = editor.document.uri.fsPath;
    const fileName = path.basename(currentFilePath, path.extname(currentFilePath));
    const csvFileName = `${fileName}_recordings.csv`;

    const csvLine = `"${text}",${startTime},${endTime},${timeTaken},${event}\n`;

    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (workspaceFolders !== undefined) {
        // const rootPath = workspaceFolders[0].uri.fsPath;
        const rootPath = "C:/Users/Admin/OneDrive/Desktop";
        const dataDir = path.join(rootPath, "StudentsLogs");

        // Check if the data directory exists, if not create one
        if (!fs.existsSync(dataDir)) {
            fs.mkdirSync(dataDir, { recursive: true });
        }

        const csvPath = path.join(dataDir, csvFileName);

        fs.appendFile(csvPath, csvLine, err => {
            if (err) {
                console.log(err);
                vscode.window.showErrorMessage('Error writing to CSV file');
            } else {
                vscode.window.showInformationMessage('Text and timestamps recorded');
                return;
            }
        });
    } else {
        vscode.window.showErrorMessage('Working folder not found, open a folder and try again.');
    }
}


function deactivate() {}

module.exports = {
    activate,
    deactivate
}
