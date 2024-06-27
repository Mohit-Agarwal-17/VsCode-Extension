const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

let inputDisposable;

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('Congratulations, your extension "Mohit" is now active!');

    let startDisposable = vscode.commands.registerCommand('Mohit.startRecording', function () {
        vscode.window.showInformationMessage('Recording started. Type your text and press Enter to log it.');

        let input = '';
        let startTime = new Date();

        inputDisposable = vscode.workspace.onDidChangeTextDocument(event => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                return;
            }
            const changes = event.contentChanges;
            if (changes.length) {
                const change = changes[0];
                if (change.text.includes(';')) {
                    vscode.window.showInformationMessage('Text captured.');
                    let endTime = new Date();
                    let timeTaken = (endTime.getTime() - startTime.getTime()) / 1000;
                    writeCsv(input, startTime.toISOString(), endTime.toISOString(), timeTaken);
                    input = '';
                    startTime = new Date();
                } else {
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

function writeCsv(text, startTime, endTime, timeTaken) {
    const csvLine = `"${text.replace(/"/g, '""')}",${startTime},${endTime},${timeTaken}\n`;

    if(vscode.workspace.workspaceFolders !== undefined) {
        let f = vscode.workspace.workspaceFolders[0].uri.fsPath ;
        
        let message = `YOUR-EXTENSION: folder: ${f}` ;
        console.log(message);
        vscode.window.showInformationMessage(message);
        const csvPath = path.join(f, 'recordings.csv');
        console.log("csvPAth: " + csvPath);
        fs.appendFile(csvPath, csvLine, err => {
            if (err) {
                console.log(err);
                vscode.window.showErrorMessage('Error writing to CSV file');
            } else {
                vscode.window.showInformationMessage('Text and timestamps recorded');
            }
        });
    } 
    else {
        let message = "YOUR-EXTENSION: Working folder not found, open a folder an try again" ;
    
        vscode.window.showErrorMessage(message);
    }
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}