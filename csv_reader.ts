//This is a CSV reader module for the XHawk Hook Test project
import fs from 'fs';
import path from 'path';
import { log } from './logger';

export function readCSV(filePath: string): string[][] {
    log(`Reading CSV file from: ${filePath}`);
    const absolutePath = path.resolve(filePath);
    try {
        const data = fs.readFileSync
        (absolutePath, 'utf8');

        const lines = data.split('\n').filter(line => line.trim() !== '');
        const result = lines.map(line => line.split(',').map(cell => cell.trim()));
        log(`Successfully read ${result.length} rows from the CSV file.`);
        return result;
    } catch (error) {
        log(`Error reading CSV file: ${error}`);
        throw error;
    }
}   