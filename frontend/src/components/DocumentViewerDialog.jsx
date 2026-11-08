import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'

export default function DocumentViewerDialog({document, onClose}){
    return(
        <Dialog open={!!document.s3_url} onOpenChange={(open) => {
            if(!open) onClose();
            }}
        >
            <DialogContent className="bg-[#15161A] w-[55vw] max-w-[98vw] h-[90vh] flex flex-col overflow-hidden">
                <DialogHeader>
                    <DialogTitle className="text-white">{document.documentTitle}</DialogTitle>
                </DialogHeader>

            <iframe 
              src={document.s3_url}
              title='Document Viewer'
              className='w-full flex-1 min-h-0 min-w-0 rounded-md'
            />
            </DialogContent>
        </Dialog>
    )
}