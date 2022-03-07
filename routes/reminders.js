import express from 'express'
import  { v4 as uuid } from 'uuid';

const router = express.Router()

const reminders = []


router.get('/', (req, res) => {
    res.send(reminders)
})


router.get('/', (req, res) => {
    res.status(200).json({todos: reminders, message: 'to-do success'})
})

//to take in new reminders and by default set them as not done
router.post('/', (req, res) => {
        const isReminderExist = reminders.findIndex((reminder) => {
            return reminder.note === req.body.note
        })
        if(isReminderExist===-1){
            const ID = uuid()
            reminders.push({
                note: req.body.note,
                dateCreated: new Date(),
                dateModified: new Date(),
                isCompleted: false,
                ID: ID 
            })

            return res.status(201).json({message:`to-do added successfully with uniqueID ${ID}`})
        }
        return res.status(401).json({message:'Note with same content already exists!!'})
})

//to delete reminder if exist accessing them via "unique id"
router.delete('/:ID', (req,res) => {
    const isID = reminders.findIndex((reminder) => {
        return reminder.ID === req.params.ID
    })
    if(isID===-1){
        reminders.filter((reminder) => {
            return reminder.ID !== req.params.ID
        })
    }
    return res.status(204).json({})
})

//to update the content or completion staus of an existing reminder 
router.patch('/:ID', (req,res) => {
    const {note, isCompleted} = req.body
    const reminder = reminders.find((reminder1) => reminder1.ID == req.params.ID)
    if(note){
        reminder.note = note
    }else if(isCompleted){
        reminder.isCompleted = isCompleted
    }else{
        res.send('Not a valid attribute!')
    }
    reminder.dateModified = new Date()
    res.send('Reminder updated successfully!')
    return res.status(200).json({})
})

export default router;